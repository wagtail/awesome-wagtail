---
name: check-links
description: Guides the automated archival workflow of awesome links. Fetching links data, moving stale entries.
license: CC0
metadata:
  audience: maintainers
  # Hide the skill from discovery: https://github.com/vercel-labs/skills#optional-fields
  internal: true
  disable-model-invocation: true
---

## Overview

Analyze and maintain links in the README. Fetches metadata for each link, detects stale entries, auto-updates GitHub repo titles and descriptions, and produces a structured report for archival decisions.

## Requirements

- **Python 3.12+** with [`uv`](https://docs.astral.sh/uv/)
- **`gh` CLI** authenticated (`gh auth status`)
- Network access for HTTP requests (httpx)

## Available scripts

- **`scripts/check_links.py`** — Fetches metadata for all links in `README.md` and generates a Markdown report on stdout.

## Workflow

### 1. Run the link checker

```bash
./scripts/check_links.py --dry-run
```

Always run with `--dry-run` first to preview changes without modifying
the README. Re-run without `--dry-run` to auto-update GitHub repo descriptions,
Resource dates and ordering when you're ready.

Resource entries ending with a date (`- \`YYYY-MM-DD\`.` etc.) are validated on
every run. The script exits with status 1 if any Resource is missing a date or
has an invalid one (wrong format, impossible calendar date, or a future date).

Add `--verbose` to see progress and API call details on stderr.

The database is stored at `.awesome-wagtail.duckdb` by default. Subsequent
runs reuse cached data (24 h for GitHub, 30 d for web pages).

### 2. Read the report

The report printed to stdout is your action plan. It contains these sections:

#### Auto-Archive Candidates (GitHub)

Repos that are **archived on GitHub** or **have not been pushed to in over
24 months**. These should be moved to `docs/archive.md` and removed from
`README.md`.

#### Needs Review — 12–24 months (GitHub)

Repos with no commits in 12–24 months. For each entry, check whether the
repo's GitHub page or its entry in `README.md` mentions "archived",
"deprecated", or "unmaintained". If so, move to archive. If the repo is
still active despite infrequent commits, leave it in place.

#### Updated Link Titles (GitHub)

Repo link titles that differ from the project name found in the repo's
README heading. Review the list — many README headings contain badge
markup or instructions rather than a clean project name. Only update
titles that are clearly better.

#### Updated Link Descriptions (GitHub)

Repo descriptions that differ from GitHub's project description. In most
cases the GitHub description is shorter and more accurate. Apply these
updates to `README.md`.

#### Resources

Summary of every Resource in the `## Resources` section: total count, missing
dates, invalid dates, and sort-order issues.

- **Missing Dates** — Resources without a trailing date. Add one.
- **Invalid Dates** — dates that are not `YYYY`, `YYYY-MM` or `YYYY-MM-DD`, not
  a real calendar date, or in the future. Fix them (the script exits non-zero).
- **Sort Order Issues** — only reported for the auto-sorted subsections listed
  below. The script reorders these automatically on a non-dry run.
- **Inferred Date Updates** — the script bumps a Resource's date when GitHub
  `pushedAt` (repos) or the page's own published/modified metadata shows a more
  recent update. Dates are never lowered, and precision is preserved (a
  `YYYY-MM` date is never replaced with a day-level one).

### Resource dates

Every item under `## Resources` ends with its **last significant update**:

```markdown
- [Wagtail Tutorials: Build Blog Step by Step](https://saashammer.com/blog/wagtail-tutorials/) - The tutorials teach you how to create a standard blog from scratch step by step - `2023-06-21`.
```

Descriptions always end with a single full stop, before the date. GitHub
descriptions are normalised automatically when they are published without
punctuation. "by Author" credits under Presentations are not treated as
descriptions.

Precision is flexible: use `YYYY-MM-DD` when known, `YYYY-MM` or `YYYY` when
only that is verifiable. Use the date of the content itself (publish date, last
meaningful revision), not the date it was added to this list.

### Ordering and per-subsection policy

Some Resources subsections age by nature and are auto-archived; others are
manually curated. Each subsection heading in `README.md` documents its own rule
in an HTML comment, which the script keeps in sync:

| Subsection      | Ordering                 | Auto-archive                  |
| --------------- | ------------------------ | ----------------------------- |
| Getting started | Latest first (automatic) | After 5 years without updates |
| Articles        | Latest first (automatic) | After 5 years without updates |
| Presentations   | Latest first (automatic) | After 5 years without updates |
| Videos          | Latest first (automatic) | After 5 years without updates |
| Podcasts        | Manual                   | Never                         |
| Showcases       | Manual                   | Never                         |
| Package lists   | Manual                   | Never                         |

The list lives in `AUTO_ARCHIVE_SUBSECTIONS` and `SUBSECTION_POLICIES` in
`scripts/check_links.py` — update both the code and this table when changing it.

### Auto-archiving Resources

Resources in the auto-archived subsections that have not been updated in the
last 5 years are moved to the matching subsection of `docs/archive.md`, keeping
their date. Entries are inserted latest first and grouped by year.

Resources in curated subsections (Podcasts, Showcases, Package lists) are never
moved automatically. If they are older than 5 years they are listed under
**Stale Manually-curated Resources** in the report for a human to review.

#### Auto-Archive Candidates (web pages)

Pages outside `## Resources` that have not been updated in over 5 years (based
on HTTP `Last-Modified` headers, `<meta>` tags, or schema.org data). Move these
to `docs/archive.md`.

#### Title Mismatches (web pages)

Page titles in `README.md` that differ from the actual `<h1>` or
`<title>` of the page. Review and update if the fetched title is a
better description of the link.

### 3. Create or update the archive file

The archive lives at `docs/archive.md`. Mirror the same section structure
as `README.md` (section > subsection). For each archived link:

1. Remove the line from `README.md`
2. Add the line under the matching section in `docs/archive.md`

Archived Resources keep their date suffix, and stay ordered latest first within
their subsection. Empty subsections use a `- None yet.` placeholder so the
Markdown and the API parser stay valid.

If the archive file does not exist yet, create it with:

```markdown
# Awesome Wagtail Archive

> Archived projects from the main README that are no longer actively maintained.

## Apps

### Blogging/news

... archived items moved here ...
```

### 4. Commit changes

When finished, review the diff and commit:

```bash
git diff
git add -A
git commit -m "check-links: archive stale entries and update metadata" --trailer "Assisted-by: <Agent harness> (<Model name>)"
```
