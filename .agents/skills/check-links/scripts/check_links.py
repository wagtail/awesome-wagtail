#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27",
#   "beautifulsoup4>=4.12",
#   "duckdb>=1.0",
#   "lxml",
# ]
# ///

"""
Check links in README.md — fetch metadata, detect stale entries, and auto-update
GitHub repo titles and descriptions.

Resources entries end with their last significant update date (`YYYY`, `YYYY-MM`,
or `YYYY-MM-DD`). These dates are validated and kept up to date, Resources are
ordered latest first within each subsection, and entries not updated in the last
5 years are archived to docs/archive.md.

Usage:
  .agents/skills/check-links/scripts/check_links.py [OPTIONS]

Options:
  --readme PATH       Path to README.md (default: README.md)
  --archive PATH      Path to docs/archive.md (default: docs/archive.md)
  --db PATH           DuckDB database path (default: .awesome-wagtail.duckdb)
  --dry-run           Don't modify files, only report
  --verbose           Print progress to stderr
  --help              Show this message
"""

import argparse
import base64
import itertools
import json
import re
import subprocess
import sys
import time
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, TypedDict

import duckdb
import httpx
from bs4 import BeautifulSoup, Tag

REPO_CACHE_MAX_AGE = timedelta(hours=24)
PAGE_CACHE_MAX_AGE = timedelta(days=30)

STALE_12_MONTHS = timedelta(days=365)
STALE_24_MONTHS = timedelta(days=730)
STALE_5_YEARS = timedelta(days=1825)

SKIP_SECTIONS = {"Contents", "Contribute", "License"}

# Resources carry a last-significant-update date, e.g. " - `2023-06-21`." or " - `2023`.".
DATED_SECTION = "Resources"
RESOURCE_DATE_PREFIX = " - `"
RESOURCE_DATE_RE = re.compile(
    rf"{re.escape(RESOURCE_DATE_PREFIX)}(\d{{4}}(?:-\d{{2}}){{0,2}})`\.$"
)
PLACEHOLDER_LINE = "- None yet."

# Resources subsections that are auto-archived when not updated recently. Other
# subsections (Showcases, Package lists, Podcasts) are manually curated and never
# auto-archived.
AUTO_ARCHIVE_SUBSECTIONS = {"Articles", "Presentations", "Videos", "Getting started"}
SORTED_SUBSECTIONS = set(AUTO_ARCHIVE_SUBSECTIONS)

AUTO_ARCHIVE_YEARS = int(STALE_5_YEARS.days / 365)
AUTO_ARCHIVE_NOTE = (
    f"Add new items at the top. Auto-archived after {AUTO_ARCHIVE_YEARS} years "
    "without updates."
)
MANUAL_NOTE = (
    "Add new items at the top. Manually curated over time, never auto-archived."
)

# Explain the sorting / archival behaviour of each subsection. These comments live
# under the subsection heading so contributors see them where they add entries.
SUBSECTION_POLICIES = {
    subsection: AUTO_ARCHIVE_NOTE for subsection in AUTO_ARCHIVE_SUBSECTIONS
} | {
    "Showcases": MANUAL_NOTE,
    "Package lists": MANUAL_NOTE,
    "Podcasts": MANUAL_NOTE,
}


def parse_date_utc(date_str: str | None) -> datetime | None:
    if not date_str:
        return None
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=UTC)
        return dt
    except (ValueError, TypeError):
        try:
            dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            return dt.replace(tzinfo=UTC)
        except (ValueError, TypeError):
            return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check links in README.md and fetch metadata."
    )
    parser.add_argument(
        "--readme",
        default="README.md",
        help="Path to README.md (default: README.md)",
    )
    parser.add_argument(
        "--archive",
        default="docs/archive.md",
        help="Path to docs/archive.md (default: docs/archive.md)",
    )
    parser.add_argument(
        "--db",
        default=".awesome-wagtail.duckdb",
        help="DuckDB database path (default: .awesome-wagtail.duckdb)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't modify files, only report",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress to stderr",
    )
    return parser.parse_args()


def log(msg: str, verbose: bool = False) -> None:
    if verbose:
        print(msg, file=sys.stderr)


# ── README Parsing (adapted from .github/api.py) ──────────────────────


class ParsedLink(TypedDict):
    name: str
    url: str
    description: str
    section: str
    subsection: str | None
    category: str
    date: str | None


def parse_line(line: str, section: str, subsection: str | None) -> ParsedLink | None:
    line = line.strip()
    if not line.startswith("- [") and not line.startswith("– ["):
        return None
    date = None
    date_match = RESOURCE_DATE_RE.search(line)
    if date_match:
        date = date_match.group(1)
        line = line[: date_match.start()]
    # Text after the link often starts with "by Author - Description", so accept anything.
    match = re.match(r"^[-–] \[([^\]]+)\]\(([^\)]+)\)(.*)$", line)
    if not match:
        return None
    name = match.group(1)
    url = match.group(2)
    description = re.sub(r"^\s*[-–]\s*", "", match.group(3)).strip()
    category = f"{section} > {subsection}" if subsection else section
    return {
        "name": name,
        "url": url,
        "description": description,
        "section": section,
        "subsection": subsection,
        "category": category,
        "date": date,
    }


def parse_readme_links(readme: str) -> list[ParsedLink]:
    lines = readme.split("\n")
    links: list[ParsedLink] = []
    current_section: str | None = None
    current_subsection: str | None = None

    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            heading = line[2:].strip()
            if heading in SKIP_SECTIONS:
                current_section = None
                current_subsection = None
            else:
                current_section = heading
                current_subsection = None
        elif line.startswith("### ") and current_section:
            current_subsection = line[4:].strip()
        elif current_section and line.startswith(("- [", "– [")):
            link = parse_line(line, current_section, current_subsection)
            if link:
                links.append(link)
    return links


# ── Resource Dates ─────────────────────────────────────────────────


def parse_resource_date(value: str) -> date | None:
    """Parse a `YYYY`, `YYYY-MM` or `YYYY-MM-DD` date, or None when invalid."""
    try:
        if re.fullmatch(r"\d{4}", value):
            return date(int(value), 1, 1)
        if re.fullmatch(r"\d{4}-\d{2}", value):
            year, month = value.split("-")
            if not 1 <= int(month) <= 12:
                return None
            return date(int(year), int(month), 1)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return date.fromisoformat(value)
    except ValueError:
        return None
    return None


def format_resource_date(value: str, day: date) -> str:
    """Format an inferred day with the same precision as the existing value."""
    if len(value) == 4:
        return f"{day.year:04d}"
    if len(value) == 7:
        return f"{day.year:04d}-{day.month:02d}"
    return day.isoformat()


def truncate_to_precision(day: date, precision: str | None) -> date:
    """Truncate a day to the precision of a date string (`YYYY`, `YYYY-MM`)."""
    if precision is None:
        return day
    if len(precision) == 4:
        return date(day.year, 1, 1)
    if len(precision) == 7:
        return date(day.year, day.month, 1)
    return day


def is_invalid_resource_date(value: str | None, today: date) -> bool:
    """Whether a Resource date is malformed, impossible, or in the future."""
    if not value:
        return False
    parsed = parse_resource_date(value)
    return parsed is None or parsed > today


def inferred_resource_date(
    link: dict[str, Any],
) -> tuple[date, str] | None:
    """Infer the last significant update of a Resource from GitHub or page metadata."""
    if link.get("link_type") == "github":
        pushed = parse_date_utc(link.get("pushed_at"))
        if pushed:
            return pushed.date(), "GitHub last push"
    if link.get("link_type") == "web" and link.get("page_date_is_content"):
        updated = parse_date_utc(link.get("page_last_updated"))
        if updated:
            return updated.date(), "page last updated"
    return None


# ── URL Classification ──────────────────────────────────────────────


def is_youtube_url(url: str) -> bool:
    return bool(re.search(r"(youtube\.com|youtu\.be)", url))


def is_github_url(url: str) -> bool:
    return bool(re.match(r"https?://github\.com/", url))


def extract_github_repo(url: str) -> tuple[str, str] | None:
    match = re.match(r"https?://github\.com/([^/]+)/([^/#\?]+)", url)
    if match:
        owner = match.group(1)
        repo = match.group(2).replace(".git", "")
        return owner, repo
    return None


# ── DuckDB Cache ──────────────────────────────────────────────────


def init_db(db_path: str) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(db_path)
    con.execute("""
        CREATE TABLE IF NOT EXISTS link_metadata (
            url VARCHAR PRIMARY KEY,
            link_type VARCHAR,
            category VARCHAR,
            fetched_at TIMESTAMP,
            repo_full_name VARCHAR,
            repo_description VARCHAR,
            star_count INTEGER,
            pushed_at VARCHAR,
            is_archived BOOLEAN,
            readme_content VARCHAR,
            project_name VARCHAR,
            topics VARCHAR,
            page_title VARCHAR,
            h1_title VARCHAR,
            meta_description VARCHAR,
            author VARCHAR,
            page_last_updated VARCHAR,
            page_date_is_content BOOLEAN
        )
    """)
    columns = {
        row[1] for row in con.execute("PRAGMA table_info('link_metadata')").fetchall()
    }
    if "page_date_is_content" not in columns:
        con.execute("ALTER TABLE link_metadata ADD COLUMN page_date_is_content BOOLEAN")
    if "topics" not in columns:
        if "tags" in columns:
            con.execute("ALTER TABLE link_metadata RENAME COLUMN tags TO topics")
        else:
            con.execute("ALTER TABLE link_metadata ADD COLUMN topics VARCHAR")
    return con


def get_cached(
    con: duckdb.DuckDBPyConnection, url: str, max_age: timedelta
) -> dict[str, Any] | None:
    row = con.execute(
        "SELECT * FROM link_metadata WHERE url = ? AND fetched_at > ?",
        [url, datetime.now(UTC) - max_age],
    ).fetchone()
    if row is None:
        return None
    columns = [desc[0] for desc in con.description]
    return dict(zip(columns, row))


def set_cached(con: duckdb.DuckDBPyConnection, url: str, data: dict[str, Any]) -> None:
    columns = list(data.keys())
    placeholders = ", ".join(["?" for _ in columns])
    col_names = ", ".join(columns)
    values = [data.get(col) for col in columns]
    con.execute(
        f"INSERT OR REPLACE INTO link_metadata ({col_names}) VALUES ({placeholders})",
        values,
    )


# ── GitHub Metadata Fetching ─────────────────────────────────────


def run_gh(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
        check=False,
    )


def fetch_github_batch(repos: list[tuple[str, str, str]]) -> dict[str, dict[str, Any]]:
    """Fetch metadata for a batch of GitHub repos via GraphQL.

    Args:
        repos: list of (url, owner, repo) tuples
    Returns:
        dict of url -> metadata dict
    """
    if not repos:
        return {}

    query_parts = []
    alias_map: dict[str, str] = {}

    for i, (url, owner, repo) in enumerate(repos):
        alias = f"r{i}"
        alias_map[alias] = url
        query_parts.append(
            f'  {alias}: repository(owner: "{owner}", name: "{repo}") {{\n'
            f"    name\n"
            f"    description\n"
            f"    stargazerCount\n"
            f"    pushedAt\n"
            f"    isArchived\n"
            f"    url\n"
            f"    repositoryTopics(first: 10) {{\n"
            f"      nodes {{\n"
            f"        topic {{\n"
            f"          name\n"
            f"        }}\n"
            f"      }}\n"
            f"    }}\n"
            f"  }}"
        )

    query = "{\n" + "\n".join(query_parts) + "\n}"
    result = run_gh(["api", "graphql", "-f", f"query={query}"])

    if result.returncode != 0:
        log(f"  GraphQL error: {result.stderr[:300]}", verbose=True)
        return {}

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        log("  JSON parse error in GraphQL response", verbose=True)
        return {}

    url_to_repo = {url: (owner, repo) for url, owner, repo in repos}

    results: dict[str, dict[str, Any]] = {}
    errors = data.get("errors", [])
    if errors:
        for err in errors:
            log(f"  GraphQL error: {err.get('message', '')}", verbose=True)

    for alias, url in alias_map.items():
        repo_data = data.get("data", {}).get(alias)
        if repo_data is None:
            results[url] = {"error": "Repository not found"}
        else:
            owner, repo_name = url_to_repo.get(url, ("", ""))
            topic_nodes = (repo_data.get("repositoryTopics") or {}).get("nodes") or []
            topics = [
                n["topic"]["name"]
                for n in topic_nodes
                if n and n.get("topic") and n["topic"].get("name")
            ]
            results[url] = {
                "repo_full_name": f"{owner}/{repo_name}"
                if owner and repo_name
                else None,
                "repo_name": repo_data.get("name"),
                "repo_description": repo_data.get("description"),
                "star_count": repo_data.get("stargazerCount"),
                "pushed_at": repo_data.get("pushedAt"),
                "is_archived": repo_data.get("isArchived"),
                "repo_url": repo_data.get("url"),
                "topics": json.dumps(topics) if topics else None,
            }

    return results


def fetch_github_readme(owner: str, repo: str) -> str | None:
    result = run_gh(["api", f"repos/{owner}/{repo}/readme"])
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout)
        if not isinstance(data, dict) or not isinstance(data.get("content"), str):
            return None
        content = data["content"]
        return base64.b64decode(content).decode("utf-8")
    except ValueError:
        return None


def extract_project_name(readme_content: str | None) -> str | None:
    if not readme_content:
        return None
    match = re.search(r"^#\s+(.+)$", readme_content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


# ── Web Page Metadata Fetching ───────────────────────────────────


def text_attribute(tag: Tag | None, attribute: str) -> str | None:
    value = tag.get(attribute) if tag else None
    return value.strip() if isinstance(value, str) and value else None


def fetch_page_metadata(url: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "page_title": None,
        "h1_title": None,
        "meta_description": None,
        "author": None,
        "page_last_updated": None,
        "page_date_is_content": False,
    }

    try:
        with httpx.Client(follow_redirects=True, timeout=15.0) as client:
            response = client.get(
                url, headers={"User-Agent": "awesome-wagtail-link-checker/1.0"}
            )
        response.raise_for_status()
    except httpx.HTTPError as e:
        metadata["error"] = str(e)
        return metadata

    soup = BeautifulSoup(response.text, "lxml")

    title_tag = soup.find("title")
    metadata["page_title"] = title_tag.get_text(strip=True) if title_tag else None

    h1 = soup.find("h1")
    metadata["h1_title"] = h1.get_text(strip=True) if h1 else None

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if (value := text_attribute(meta_desc, "content")) is not None:
        metadata["meta_description"] = value
    else:
        meta_og_desc = soup.find("meta", attrs={"property": "og:description"})
        if (value := text_attribute(meta_og_desc, "content")) is not None:
            metadata["meta_description"] = value

    metadata["author"] = find_author(soup)

    page_date, page_date_is_content = find_last_updated(soup, response)
    metadata["page_last_updated"] = page_date
    metadata["page_date_is_content"] = page_date_is_content

    return metadata


def find_author(soup: BeautifulSoup) -> str | None:
    meta_author = soup.find("meta", attrs={"name": "author"})
    if (value := text_attribute(meta_author, "content")) is not None:
        return value

    twitter_creator = soup.find("meta", attrs={"name": "twitter:creator"})
    if (value := text_attribute(twitter_creator, "content")) is not None:
        return value

    article_author = soup.find("meta", attrs={"property": "article:author"})
    if (value := text_attribute(article_author, "content")) is not None:
        return value

    rel_author = soup.find("link", attrs={"rel": "author"})
    if (value := text_attribute(rel_author, "href")) is not None:
        return value

    for script in soup.find_all("script", type="application/ld+json"):
        if script.string is None:
            continue
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                author = data.get("author", {})
                if isinstance(author, dict):
                    return author.get("name")
                elif isinstance(author, str):
                    return author
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        author = item.get("author", {})
                        if isinstance(author, dict):
                            return author.get("name")
        except (json.JSONDecodeError, AttributeError):
            pass

    return None


def find_last_updated(
    soup: BeautifulSoup, response: httpx.Response
) -> tuple[str | None, bool]:
    """Find the page's last updated date, and whether it is a real content date."""
    for meta_name in ("date", "revised", "dcterms.modified"):
        meta = soup.find("meta", attrs={"name": meta_name})
        if (value := text_attribute(meta, "content")) is not None:
            return value, True

    for meta_prop in ("article:modified_time", "article:published_time"):
        meta = soup.find("meta", attrs={"property": meta_prop})
        if (value := text_attribute(meta, "content")) is not None:
            return value, True

    time_tag = soup.find("time", attrs={"datetime": True})
    if (value := text_attribute(time_tag, "datetime")) is not None:
        return value, True

    for script in soup.find_all("script", type="application/ld+json"):
        if script.string is None:
            continue
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                modified = data.get("dateModified") or data.get("datePublished")
                if modified:
                    return modified, True
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        modified = item.get("dateModified") or item.get("datePublished")
                        if modified:
                            return modified, True
        except (json.JSONDecodeError, AttributeError):
            pass

    # Last-Modified headers usually reflect CDN caching rather than content changes,
    # so they are only used as a last resort and never to bump a Resource date.
    if "last-modified" in response.headers:
        return response.headers["last-modified"], False

    return None, False


# ── README Auto-Update for GitHub Repos ──────────────────────────


def ensure_full_stop(description: str) -> str:
    """Make a description end with exactly one full stop.

    Upstream GitHub descriptions often have no trailing punctuation, or end with
    "!" / "?". Descriptions may end with inline code, so only trailing "!" and "?"
    are normalised, and an existing full stop is never duplicated.
    """
    description = description.rstrip()
    if not description or description.endswith("."):
        return description
    if description.endswith(":"):
        # Truncated upstream descriptions ("... sources. Docs:") read wrong with a
        # full stop glued to the colon.
        return f"{description} ..."
    return description.rstrip("!?") + "."


def auto_update_readme_lines(
    lines: list[str],
    updates: list[dict[str, str | None]],
) -> list[str]:
    updated = list(lines)
    for upd in updates:
        old_url = upd["url"]
        if not old_url:
            continue
        new_title = upd.get("new_title")
        new_desc = upd.get("new_description")
        new_date = upd.get("new_date")
        for i, line in enumerate(updated):
            # Match the link URL exactly: a substring match would make
            # https://github.com/owner/repo also hit owner/repo-other.
            link_match = re.match(
                r"^(\s*[-–]\s*)\[([^\]]+)\]\(([^\)]+)\)(.*)$", line.strip()
            )
            if not link_match or link_match.group(3) != old_url:
                continue
            rest = re.sub(r" - `\d{4}(?:-\d{2}){0,2}`\.$", "", link_match.group(4))
            old_date = None
            date_match = RESOURCE_DATE_RE.search(line)
            if date_match:
                old_date = date_match.group(1)
            prefix = link_match.group(1)
            old_desc = re.sub(r"^\s*[-–]\s*", "", rest).strip()
            title = new_title or link_match.group(2)
            desc = ensure_full_stop(new_desc if new_desc else old_desc)
            suffix = (
                f"{RESOURCE_DATE_PREFIX}{new_date or old_date}`."
                if old_date or new_date
                else ""
            )
            updated[i] = (
                f"{prefix}[{title}]({old_url})"
                + (f" - {desc}" if desc else "")
                + suffix
            )
    return updated


COMMENT_RE = re.compile(r"^\s*<!--.*-->\s*$")


def policy_comment(subsection: str) -> str | None:
    note = SUBSECTION_POLICIES.get(subsection)
    return f"<!-- {note} -->" if note else None


def reorder_resource_subsections(
    readme: str, links: list[dict[str, Any]], section: str = DATED_SECTION
) -> str:
    """Sort each dated subsection latest first, keep placeholders and policy comments.

    Comments documenting sorting / archival behaviour are inserted (or refreshed)
    directly under each subsection heading.
    """
    dates = {
        link["url"]: link.get("date") or ""
        for link in links
        if link.get("section") == section
    }
    lines = readme.split("\n")
    output: list[str] = []
    in_section = False
    block: list[str] | None = None
    subsection: str | None = None

    def flush() -> None:
        if block is None:
            return
        entries = [b for b in block if b.startswith(("- [", "– ["))]
        others = [
            b
            for b in block
            if b.strip()
            and not b.startswith(("- [", "– ["))
            and not COMMENT_RE.match(b)
        ]
        if subsection in SORTED_SUBSECTIONS:
            # Latest first. Stable sort: entries with the same date keep their order.
            entries.sort(key=lambda b: dates.get(_extract_url(b)) or "", reverse=True)
        if not entries and not others:
            entries = [PLACEHOLDER_LINE]
        comment = policy_comment(subsection) if subsection else None
        output.extend([""] + ([comment] if comment else []) + [""] + others + entries)
        output.append("")

    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            flush()
            block = None
            in_section = line[2:].strip() == section
            output.append(line)
        elif in_section and line.startswith("### "):
            flush()
            block = []
            subsection = line[4:].strip()
            output.append(line)
        elif block is not None:
            block.append(line)
        else:
            output.append(line)
    flush()

    # Collapse the trailing blank lines flush() adds before the next heading.
    result: list[str] = []
    for line in output:
        if line == "" and result and result[-1] == "":
            continue
        result.append(line)
    return "\n".join(result)


def _date_suffix_of(entry: str) -> str:
    match = RESOURCE_DATE_RE.search(entry)
    return match.group(1) if match else ""


def _extract_url(entry: str) -> str:
    match = re.match(r"^[-–] \[[^\]]+\]\(([^\)]+)\)", entry.strip())
    return match.group(1) if match else ""


def auto_archive_resources(
    readme: str,
    archive: str,
    links: list[dict[str, Any]],
    today: datetime,
) -> tuple[str, str, list[dict[str, Any]]]:
    """Move stale Resources into docs/archive.md, keeping their dates.

    Only subsections listed in AUTO_ARCHIVE_SUBSECTIONS are archived; the others are
    manually curated and only reported as stale.
    """
    cutoff = today.date() - STALE_5_YEARS
    stale: list[dict[str, Any]] = []
    for link in links:
        if link.get("section") != DATED_SECTION or not link.get("date"):
            continue
        if link.get("subsection") not in AUTO_ARCHIVE_SUBSECTIONS:
            continue
        parsed = parse_resource_date(link["date"])
        if parsed and parsed < cutoff:
            stale.append(link)

    if not stale:
        return readme, archive, []

    stale_urls = {link["url"] for link in stale}

    readme_lines = readme.split("\n")
    archive_lines = archive.split("\n")
    current_section: str | None = None
    current_subsection: str | None = None
    archive_targets: dict[str, int] = {}

    for i, line in enumerate(archive_lines):
        if line.startswith("## ") and not line.startswith("### "):
            current_section = line[2:].strip()
            current_subsection = None
        elif line.startswith("### ") and current_section == DATED_SECTION:
            current_subsection = line[4:].strip()
            archive_targets[current_subsection] = i
    if DATED_SECTION not in archive:
        raise ValueError(
            f"{DATED_SECTION} section not found in the archive, cannot archive resources"
        )

    moved_lines: list[str] = []
    kept_readme: list[str] = []
    in_resources = False
    for line in readme_lines:
        if line.startswith("## ") and not line.startswith("### "):
            in_resources = line[2:].strip() == DATED_SECTION
        if in_resources and _extract_url(line) in stale_urls:
            moved_lines.append(line)
            continue
        kept_readme.append(line)

    # Insert moved entries under their matching archive subsection, latest first.
    for link in stale:
        url = link["url"]
        line = next(l for l in moved_lines if _extract_url(l) == url)
        subsection = link.get("subsection") or "Articles"
        if subsection not in archive_targets:
            archive_lines.append("")
            archive_lines.append(f"### {subsection}")
            archive_lines.append("")
            archive_targets[subsection] = len(archive_lines) - 1
        start = archive_targets[subsection] + 1
        end = start
        while end < len(archive_lines) and not archive_lines[end].startswith(
            ("## ", "### ")
        ):
            end += 1
        block = archive_lines[start:end]
        entries = [b for b in block if b.startswith(("- [", "– ["))]
        if line not in entries:
            entries.append(line)
        # Latest first. Blank lines group entries by year, so insert the new entry
        # at the right position and keep the existing year-group layout.
        entries.sort(key=_date_suffix_of, reverse=True)
        grouped: list[str] = []
        previous_year = None
        for entry in entries:
            year = _date_suffix_of(entry)[:4]
            if previous_year is not None and year != previous_year:
                grouped.append("")
            grouped.append(entry)
            previous_year = year
        # Only the contiguous run from the first to the last entry is rewritten, so
        # the surrounding layout (blank lines between subsections) is preserved.
        entry_indexes = [i for i, b in enumerate(block) if b.startswith(("- [", "– ["))]
        first = min(entry_indexes)
        last = max(entry_indexes)
        new_block = block[:first] + grouped + block[last + 1 :]
        delta = len(new_block) - len(block)
        archive_lines[start:end] = new_block
        # Headings after the edited block shift by delta.
        for key, value in archive_targets.items():
            if value >= end:
                archive_targets[key] = value + delta
        archive_targets[subsection] = start - 1

    readme_out = "\n".join(kept_readme).rstrip("\n") + "\n"
    archive_out = "\n".join(archive_lines).rstrip("\n") + "\n"
    return readme_out, archive_out, stale


# ── Report Generation ─────────────────────────────────────────────


def generate_resources_report(
    links: list[dict[str, Any]],
    today: datetime,
) -> str:
    """Report date issues and inferred date updates for Resources."""
    resources = [l for l in links if l.get("section") == DATED_SECTION]
    lines: list[str] = []
    if not resources:
        return ""

    missing = [l for l in resources if not l.get("date")]
    invalid = [
        l for l in resources if is_invalid_resource_date(l.get("date"), today.date())
    ]
    date_updates = [l for l in resources if l.get("new_date")]

    # Ordering: auto-sorted subsections must be sorted latest first.
    out_of_order: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for subsection in dict.fromkeys(l.get("subsection") for l in resources):
        if subsection not in SORTED_SUBSECTIONS:
            continue
        entries = [
            l
            for l in resources
            if l.get("subsection") == subsection
            and parse_resource_date(l.get("date") or "")
        ]
        for previous, current in itertools.pairwise(entries):
            prev_date = parse_resource_date(previous["date"])
            cur_date = parse_resource_date(current["date"])
            if prev_date and cur_date and cur_date > prev_date:
                out_of_order.append((subsection, previous, current))

    lines.append("## Resources\n")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Resources | {len(resources)} |")
    lines.append(f"| Missing dates | {len(missing)} |")
    lines.append(f"| Invalid dates | {len(invalid)} |")
    lines.append(f"| Sort order issues | {len(out_of_order)} |")
    lines.append(f"| Inferred date updates | {len(date_updates)} |\n")

    if missing:
        lines.append("### Missing Dates\n")
        lines.append("| # | Link | Category |")
        lines.append("|---|------|----------|")
        for i, link in enumerate(missing, 1):
            lines.append(
                f"| {i} | [{link['name']}]({link['url']}) | {link.get('category', '')} |"
            )
        lines.append("")

    if invalid:
        lines.append("### Invalid Dates\n")
        lines.append(
            "Dates must be `YYYY`, `YYYY-MM` or `YYYY-MM-DD`, a real calendar date, "
            "and not in the future.\n"
        )
        lines.append("| # | Link | Date | Category |")
        lines.append("|---|------|------|----------|")
        for i, link in enumerate(invalid, 1):
            lines.append(
                f"| {i} | [{link['name']}]({link['url']}) | {link['date']} | {link.get('category', '')} |"
            )
        lines.append("")

    if out_of_order:
        lines.append("### Sort Order Issues\n")
        lines.append("Resources are ordered latest first within each subsection.\n")
        lines.append("| # | Subsection | Before | After |")
        lines.append("|---|------------|--------|-------|")
        for i, (subsection, previous, current) in enumerate(out_of_order, 1):
            lines.append(
                f"| {i} | {subsection} | {previous['name']} ({previous['date']}) | "
                f"{current['name']} ({current['date']}) |"
            )
        lines.append("")

    if date_updates:
        lines.append("### Inferred Date Updates\n")
        lines.append(
            "Dates were updated when the resource was found to have changed since its listed date.\n"
        )
        lines.append("| # | Link | Old Date | New Date | Source |")
        lines.append("|---|------|----------|----------|--------|")
        for i, link in enumerate(date_updates, 1):
            lines.append(
                f"| {i} | [{link['name']}]({link['url']}) | {link.get('date', '')} | "
                f"{link['new_date']} | {link.get('new_date_source', '')} |"
            )
        lines.append("")

    return "\n".join(lines)


def generate_archive_report(
    stale: list[dict[str, Any]],
    today: datetime,
    curated_stale: list[dict[str, Any]] | None = None,
) -> str:
    lines: list[str] = []
    if stale:
        lines.append("## Archived Resources\n")
        lines.append(
            f"{len(stale)} Resources had not been updated in the last {AUTO_ARCHIVE_YEARS} years "
            "and were moved to docs/archive.md.\n"
        )
        lines.append("| # | Link | Date | Category |")
        lines.append("|---|------|------|----------|")
        for i, link in enumerate(stale, 1):
            lines.append(
                f"| {i} | [{link['name']}]({link['url']}) | {link['date']} | {link.get('category', '')} |"
            )
        lines.append("")
    if curated_stale:
        lines.append("### Stale Manually-curated Resources\n")
        lines.append(
            "These Resources are not auto-archived but have not been updated in the last "
            f"{AUTO_ARCHIVE_YEARS} years. Review them manually.\n"
        )
        lines.append("| # | Link | Date | Category |")
        lines.append("|---|------|------|----------|")
        for i, link in enumerate(curated_stale, 1):
            lines.append(
                f"| {i} | [{link['name']}]({link['url']}) | {link['date']} | {link.get('category', '')} |"
            )
        lines.append("")
    return "\n".join(lines)


def generate_report(
    all_links: list[dict[str, Any]],
    today: datetime,
) -> str:
    lines: list[str] = []
    lines.append("# Link Check Report\n")
    lines.append(f"Generated: {today.isoformat()}\n")

    gh_repos = [l for l in all_links if l.get("link_type") == "github"]
    web_links = [l for l in all_links if l.get("link_type") == "web"]
    youtube_links = [l for l in all_links if l.get("link_type") == "youtube"]
    errors = [l for l in all_links if l.get("error")]

    lines.append("## Summary\n")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Total links | {len(all_links)} |")
    lines.append(f"| GitHub repos | {len(gh_repos)} |")
    lines.append(f"| Web pages | {len(web_links)} |")
    lines.append(f"| YouTube (skipped) | {len(youtube_links)} |")
    lines.append(f"| Errors | {len(errors)} |\n")

    if gh_repos:
        lines.append("## GitHub Repos\n")

        auto_archive = []
        needs_review = []
        active = []
        title_updates = []

        for link in gh_repos:
            pushed_at = link.get("pushed_at")
            is_archived = link.get("is_archived", False)
            stale_date = None
            pushed_date = parse_date_utc(pushed_at)
            if pushed_date:
                stale_date = today - pushed_date

            if link.get("new_title") and link["new_title"] != link.get("name"):
                title_updates.append(link)

            if is_archived or stale_date and stale_date > STALE_24_MONTHS:
                auto_archive.append(link)
            elif stale_date and stale_date > STALE_12_MONTHS:
                needs_review.append(link)
            else:
                active.append(link)

        if auto_archive:
            lines.append(f"### Auto-Archive Candidates ({len(auto_archive)})\n")
            lines.append(
                "These repos are archived or have not been updated in over 24 months.\n"
            )
            lines.append("| # | Link | Stars | Last Commit | Archived | Category |")
            lines.append("|---|------|-------|-------------|----------|----------|")
            for i, link in enumerate(auto_archive, 1):
                stars = link.get("star_count") or "?"
                pushed = (link.get("pushed_at") or "?")[:10]
                arch = "Yes" if link.get("is_archived") else "No"
                url = link["url"]
                title = link.get("name", "")
                desc = link.get("description", "")
                link_text = f"[{title}]({url})" + (f" - {desc}" if desc else "")
                lines.append(
                    f"| {i} | {link_text} | {stars} | {pushed} | {arch} | {link.get('category', '')} |"
                )
            lines.append("")

        if needs_review:
            lines.append(f"### Needs Review — 12–24 months ({len(needs_review)})\n")
            lines.append(
                "These repos have not been updated in 12–24 months. Check if they mention 'archived' or 'deprecated'.\n"
            )
            lines.append("| # | Link | Stars | Last Commit | Category |")
            lines.append("|---|------|-------|-------------|----------|")
            for i, link in enumerate(needs_review, 1):
                stars = link.get("star_count") or "?"
                pushed = (link.get("pushed_at") or "?")[:10]
                url = link["url"]
                title = link.get("name", "")
                desc = link.get("description", "")
                link_text = f"[{title}]({url})" + (f" - {desc}" if desc else "")
                lines.append(
                    f"| {i} | {link_text} | {stars} | {pushed} | {link.get('category', '')} |"
                )
            lines.append("")

        if active:
            lines.append(f"### Active Repos ({len(active)})\n")
            lines.append("| # | Link | Stars | Last Commit | Archived | Category |")
            lines.append("|---|------|-------|-------------|----------|----------|")
            for i, link in enumerate(active, 1):
                stars = link.get("star_count") or "?"
                pushed = (link.get("pushed_at") or "?")[:10]
                arch = "Yes" if link.get("is_archived") else "No"
                url = link["url"]
                title = link.get("name", "")
                desc = link.get("description", "")
                link_text = f"[{title}]({url})" + (f" - {desc}" if desc else "")
                lines.append(
                    f"| {i} | {link_text} | {stars} | {pushed} | {arch} | {link.get('category', '')} |"
                )
            lines.append("")

        if title_updates:
            lines.append(f"### Updated Link Titles ({len(title_updates)})\n")
            lines.append(
                "The following GitHub repo links had titles auto-updated to match their README project name.\n"
            )
            lines.append("| URL | Old Title | New Title |")
            lines.append("|-----|-----------|-----------|")
            for link in title_updates:
                lines.append(
                    f"| {link['url']} | {link.get('name', '')} | {link.get('new_title', '')} |"
                )
            lines.append("")

        if title_updates:
            lines.append(f"### Updated Link Descriptions ({len(title_updates)})\n")
            lines.append(
                "The following GitHub repo links had descriptions auto-updated to match the GitHub project description.\n"
            )
            lines.append("| URL | Old Description | New Description |")
            lines.append("|-----|-----------------|-----------------|")
            for link in title_updates:
                old_desc = link.get("description", "")
                new_desc = link.get("repo_description", "") or "(none)"
                if old_desc != new_desc:
                    lines.append(f"| {link['url']} | {old_desc} | {new_desc} |")
            lines.append("")

    if web_links:
        lines.append("## Other Links\n")

        auto_archive_web = []
        title_mismatches = []

        for link in web_links:
            last_updated = link.get("page_last_updated")
            updated_date = parse_date_utc(last_updated)
            if updated_date and today - updated_date > STALE_5_YEARS:
                auto_archive_web.append(link)

            page_title = link.get("h1_title") or link.get("page_title")
            old_title = link.get("name", "")
            if (
                page_title
                and old_title
                and old_title not in page_title
                and page_title not in old_title
            ):
                title_mismatches.append(link)

        if auto_archive_web:
            lines.append(
                f"### Auto-Archive Candidates — 5+ years ({len(auto_archive_web)})\n"
            )
            lines.append("These pages have not been updated in over 5 years.\n")
            lines.append("| # | URL | Title | Last Updated | Category |")
            lines.append("|---|-----|-------|-------------|----------|")
            for i, link in enumerate(auto_archive_web, 1):
                title = (
                    link.get("h1_title")
                    or link.get("page_title")
                    or link.get("name", "")
                )
                updated = (link.get("page_last_updated") or "?")[:10]
                url = link["url"]
                lines.append(
                    f"| {i} | [{title}]({url}) | {title} | {updated} | {link.get('category', '')} |"
                )
            lines.append("")

        if title_mismatches:
            lines.append(f"### Title Mismatches ({len(title_mismatches)})\n")
            lines.append("The README link title differs from the page title.\n")
            lines.append("| # | URL | README Title | Page Title |")
            lines.append("|---|-----|-------------|------------|")
            for i, link in enumerate(title_mismatches, 1):
                page_title = link.get("h1_title") or link.get("page_title") or ""
                lines.append(
                    f"| {i} | {link['url']} | {link.get('name', '')} | {page_title} |"
                )
            lines.append("")

    if errors:
        lines.append("## Errors\n")
        lines.append("| URL | Error |")
        lines.append("|-----|-------|")
        for link in errors:
            lines.append(f"| {link['url']} | {link.get('error', 'Unknown')} |")
        lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()
    verbose = args.verbose
    dry_run = args.dry_run

    readme_path = Path(args.readme)
    if not readme_path.exists():
        print(f"Error: README not found at {readme_path}", file=sys.stderr)
        sys.exit(1)

    log(f"Reading {readme_path}...", verbose)
    readme = readme_path.read_text(encoding="utf-8")

    log("Parsing links...", verbose)
    links = parse_readme_links(readme)
    log(f"  Found {len(links)} links", verbose)

    log("Initializing DuckDB cache...", verbose)
    con = init_db(args.db)

    today = datetime.now(UTC)

    classified_links: list[dict[str, Any]] = []

    for parsed_link in links:
        link: dict[str, Any] = dict(parsed_link)
        url = link["url"]
        if is_youtube_url(url):
            link["link_type"] = "youtube"
            classified_links.append(link)
            continue

        if is_github_url(url):
            link["link_type"] = "github"
        else:
            link["link_type"] = "web"
        classified_links.append(link)

    # ── Fetch GitHub metadata ──────────────────────────────

    gh_links = [l for l in classified_links if l["link_type"] == "github"]
    non_cached_gh: list[dict[str, Any]] = []

    for link in gh_links:
        cached = get_cached(con, link["url"], REPO_CACHE_MAX_AGE)
        if cached:
            link.update(cached)
            link["from_cache"] = True
            log(f"  [cache] {link['url']}", verbose)
        else:
            link["from_cache"] = False
            non_cached_gh.append(link)

    if non_cached_gh:
        log(f"Fetching metadata for {len(non_cached_gh)} GitHub repos...", verbose)
        repo_batches: list[tuple[str, str, str]] = []
        for link in non_cached_gh:
            repo = extract_github_repo(link["url"])
            if repo:
                repo_batches.append((link["url"], repo[0], repo[1]))

        BATCH_SIZE = 50
        for i in range(0, len(repo_batches), BATCH_SIZE):
            batch = repo_batches[i : i + BATCH_SIZE]
            log(
                f"  Batch {i // BATCH_SIZE + 1}/{(len(repo_batches) + BATCH_SIZE - 1) // BATCH_SIZE}",
                verbose,
            )
            batch_results = fetch_github_batch(batch)

            for link in non_cached_gh:
                if link["url"] in batch_results:
                    result = batch_results[link["url"]]
                    if "error" in result:
                        link["error"] = result["error"]
                    else:
                        link.update(result)

            for url, owner, repo in batch:
                result = batch_results.get(url, {})
                if "error" in result:
                    continue

                log(f"  Fetching README for {owner}/{repo}...", verbose)
                readme_content = fetch_github_readme(owner, repo)
                if readme_content:
                    matching_link = next(
                        (l for l in non_cached_gh if l["url"] == url), None
                    )
                    if matching_link is not None:
                        matching_link["readme_content"] = readme_content
                        matching_link["project_name"] = extract_project_name(
                            readme_content
                        )

                time.sleep(0.1)

        for link in non_cached_gh:
            cache_data = {
                "url": link["url"],
                "link_type": "github",
                "category": link.get("category", ""),
                "fetched_at": datetime.now(UTC),
                "repo_full_name": link.get("repo_full_name"),
                "repo_description": link.get("repo_description"),
                "star_count": link.get("star_count"),
                "pushed_at": link.get("pushed_at"),
                "is_archived": link.get("is_archived"),
                "readme_content": link.get("readme_content"),
                "project_name": link.get("project_name"),
                "topics": link.get("topics"),
            }
            set_cached(con, link["url"], cache_data)

    # ── Fetch web page metadata ────────────────────────────

    web_links = [l for l in classified_links if l["link_type"] == "web"]
    non_cached_web: list[dict[str, Any]] = []

    for link in web_links:
        cached = get_cached(con, link["url"], PAGE_CACHE_MAX_AGE)
        if cached:
            link.update(cached)
            link["from_cache"] = True
            log(f"  [cache] {link['url']}", verbose)
        else:
            link["from_cache"] = False
            non_cached_web.append(link)

    if non_cached_web:
        log(f"Fetching metadata for {len(non_cached_web)} web pages...", verbose)
        for link in non_cached_web:
            log(f"  Fetching {link['url']}...", verbose)
            page_data = fetch_page_metadata(link["url"])
            link.update(page_data)
            if "error" in page_data:
                log(f"    Error: {page_data['error']}", verbose)

            cache_data = {
                "url": link["url"],
                "link_type": "web",
                "category": link.get("category", ""),
                "fetched_at": datetime.now(UTC),
                "page_title": page_data.get("page_title"),
                "h1_title": page_data.get("h1_title"),
                "meta_description": page_data.get("meta_description"),
                "author": page_data.get("author"),
                "page_last_updated": page_data.get("page_last_updated"),
                "page_date_is_content": page_data.get("page_date_is_content"),
            }
            set_cached(con, link["url"], cache_data)

            time.sleep(0.2)

    # ── Determine updates for GitHub repos ─────────────────

    desc_updates: list[dict[str, str | None]] = []
    for link in gh_links:
        new_title = link.get("project_name") or link.get("repo_name")
        new_desc = link.get("repo_description")
        if new_title and new_title != link.get("name"):
            link["new_title"] = new_title
        if new_desc and new_desc != link.get("description"):
            link["new_description"] = new_desc
            desc_updates.append(
                {
                    "url": link["url"],
                    "new_description": new_desc,
                }
            )

    # ── Infer Resource dates ───────────────────────────────

    for link in classified_links:
        if link.get("section") != DATED_SECTION or not link.get("date"):
            continue
        inferred = inferred_resource_date(link)
        if inferred is None:
            continue
        inferred_day, source = inferred
        existing_day = parse_resource_date(link["date"])
        if existing_day is None:
            continue
        # Only bump dates: never lower a date, and keep the existing precision.
        if truncate_to_precision(inferred_day, link["date"]) > existing_day:
            link["new_date"] = format_resource_date(link["date"], inferred_day)
            link["new_date_source"] = source

    date_updates: list[dict[str, str | None]] = [
        {
            "url": link["url"],
            "new_description": link.get("new_description"),
            "new_title": link.get("new_title"),
            "new_date": link["new_date"],
        }
        for link in classified_links
        if link.get("new_date")
    ]

    # ── Auto-update README (descriptions only, titles are LLM-reviewable) ──

    if desc_updates and not dry_run:
        log(
            f"Updating {len(desc_updates)} GitHub link descriptions in README...",
            verbose,
        )
        readme_lines = readme.split("\n")
        updated_lines = auto_update_readme_lines(readme_lines, desc_updates)
        readme = "\n".join(updated_lines)
        log("  README descriptions updated.", verbose)

    if date_updates and not dry_run:
        log(f"Updating {len(date_updates)} Resource dates in README...", verbose)
        readme_lines = readme.split("\n")
        updated_lines = auto_update_readme_lines(readme_lines, date_updates)
        readme = "\n".join(updated_lines)

    if not dry_run:
        readme = reorder_resource_subsections(readme, classified_links)

    # ── Auto-archive Resources older than 5 years ──────────

    archive_path = Path(args.archive)
    stale_resources: list[dict[str, Any]] = []
    if archive_path.exists():
        archive = archive_path.read_text(encoding="utf-8")
        new_readme, new_archive, stale_resources = auto_archive_resources(
            readme, archive, classified_links, today
        )
        if stale_resources and not dry_run:
            log(
                f"Archiving {len(stale_resources)} stale Resources...",
                verbose,
            )
            readme = new_readme
            archive_path.write_text(new_archive, encoding="utf-8")
            # Keep the README subsections sorted after removals.
            readme = reorder_resource_subsections(readme, classified_links)

    if not dry_run:
        readme_path.write_text(readme, encoding="utf-8")

    # ── Generate report ─────────────────────────────────────

    report = generate_report(classified_links, today)
    resources_report = generate_resources_report(classified_links, today)
    archive_cutoff = today.date() - STALE_5_YEARS
    curated_stale = [
        link
        for link in classified_links
        if link.get("section") == DATED_SECTION
        and link.get("subsection") not in AUTO_ARCHIVE_SUBSECTIONS
        and (day := parse_resource_date(link.get("date") or ""))
        and day < archive_cutoff
    ]
    archive_report = generate_archive_report(stale_resources, today, curated_stale)
    print(report)
    if resources_report:
        print(resources_report)
    if archive_report:
        print(archive_report)

    # ── Exit with an error for invalid Resources dates or ordering ──

    invalid_dates = [
        l
        for l in classified_links
        if l.get("section") == DATED_SECTION
        and is_invalid_resource_date(l.get("date"), today.date())
    ]
    missing_dates = [
        l
        for l in classified_links
        if l.get("section") == DATED_SECTION and not l.get("date")
    ]
    has_resource_errors = bool(invalid_dates or missing_dates)

    # ── Print cache stats ───────────────────────────────────

    counts = dict(
        con.execute(
            "SELECT link_type, COUNT(*) FROM link_metadata GROUP BY link_type"
        ).fetchall()
    )
    log(
        f"\nCache stats: {counts.get('github', 0)} GitHub repos, {counts.get('web', 0)} web pages stored in {args.db}",
        verbose,
    )

    con.close()

    if has_resource_errors:
        print(
            "Error: Resources have missing or invalid dates. See the Resources report above.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
