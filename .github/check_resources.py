# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Validate the Resource entries in README.md: every item under "Resources" must
end with a valid `YYYY`, `YYYY-MM` or `YYYY-MM-DD` date, entries within a sorted
subsection must be ordered latest first, each subsection must document its
sorting / archival policy in an HTML comment, empty subsections must use a
"- None yet." placeholder, and descriptions must end with a full stop.

Runs as part of CI. See docs/CONTRIBUTING.md and the check-links skill.
"""

import itertools
import re
import sys
from datetime import UTC, date, datetime
from pathlib import Path

README_PATH = Path(__file__).resolve().parent.parent / "README.md"

SECTION = "Resources"

# Subsections sorted latest first by the check-links script.
SORTED_SUBSECTIONS = {"Getting started", "Articles", "Presentations", "Videos"}

DATE_SUFFIX_RE = re.compile(r" - `(\d{4}(?:-\d{2}){0,2})`\.$")
ENTRY_RE = re.compile(r"^[-–] \[[^\]]+\]\([^)]+\)(.*)$")
PLACEHOLDER_LINE = "- None yet."
POLICY_COMMENT_RE = re.compile(r"^\s*<!--.*-->\s*$")


def parse_date(value: str) -> date | None:
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


def description_of(line: str) -> str:
    """The description text of a Resource entry, without its date suffix."""
    match = ENTRY_RE.match(line)
    rest = DATE_SUFFIX_RE.sub("", match.group(1) if match else "")
    return re.sub(r"^\s*[-–]\s*", "", rest).strip()


def main() -> int:
    readme = README_PATH.read_text(encoding="utf-8")
    if f"## {SECTION}\n" not in readme:
        print(f"Error: No '## {SECTION}' section in {README_PATH}", file=sys.stderr)
        return 1

    section = readme.split(f"## {SECTION}\n", 1)[1].split("\n## ", 1)[0]
    today = datetime.now(UTC).date()

    errors: list[str] = []
    items: dict[str, list[tuple[str, str]]] = {}
    has_comment: dict[str, bool] = {}
    has_placeholder: dict[str, bool] = {}
    current: str | None = None

    for line in section.split("\n"):
        if line.startswith("### "):
            current = line[4:].strip()
            items[current] = []
            has_comment[current] = False
            has_placeholder[current] = False
        elif current is not None and POLICY_COMMENT_RE.match(line):
            has_comment[current] = True
        elif current is not None and line.strip() == PLACEHOLDER_LINE:
            has_placeholder[current] = True
        elif current is not None and line.startswith(("- [", "– [")):
            match = DATE_SUFFIX_RE.search(line)
            if not match:
                errors.append(f"Missing date under '{current}': {line.strip()}")
                continue
            value = match.group(1)
            parsed = parse_date(value)
            if parsed is None:
                errors.append(
                    f"Invalid date `{value}` under '{current}': {line.strip()}"
                )
                continue
            if parsed > today:
                errors.append(
                    f"Future date `{value}` under '{current}': {line.strip()}"
                )
            description = description_of(line)
            # "by Author" credits (Presentations) are not sentences.
            if (
                description
                and not description.startswith("by ")
                and not description.endswith(".")
            ):
                errors.append(
                    f"Description must end with a full stop under '{current}': "
                    f"{line.strip()}"
                )
            items[current].append((value, line.strip()))

    for subsection, entries in items.items():
        if not has_comment[subsection]:
            errors.append(f"Missing policy comment under '### {subsection}'")
        if not entries and not has_placeholder[subsection]:
            errors.append(
                f"Empty subsection '### {subsection}' needs a '{PLACEHOLDER_LINE}' line"
            )
        if subsection not in SORTED_SUBSECTIONS:
            continue
        for previous, current_entry in itertools.pairwise(entries):
            if current_entry[0] > previous[0]:
                errors.append(
                    f"'{subsection}' is not sorted latest first: "
                    f"`{previous[0]}` comes before `{current_entry[0]}`"
                )

    if errors:
        print("Resource validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("Resource validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
