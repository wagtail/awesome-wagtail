# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
This script parses the README.md and generates a machine-readable
data structure from it, for publication as an API.

https://wagtail.github.io/awesome-wagtail/api/v1/readme.json

It is automatically ran as part of Travis builds, also validating the README
formatting, and the API endpoint is deployed on successful builds on master.

See also:
- https://djangopackages.org/api/v3/grids/wagtail-cms/
- https://github.com/awesomerank/rank
"""

import json
from datetime import UTC, datetime
from pathlib import Path

API_PATH = "/api/v1/readme.json"

# Resources end with their last significant update, e.g. " - `2023-06-21`." or " - `2023`."
DATE_SUFFIX_SEPARATOR = " - `"


def parse_line(line: str, category: str, dated: bool = False) -> dict:
    """Parse a single line from the README into a structured dictionary."""
    print(line)
    date = None
    if dated:
        # Dates are validated by the check-links script and CI.
        line, _, date = line.rpartition(DATE_SUFFIX_SEPARATOR)
        date = date.rstrip(".")[:-1]

    name = line.split("](")[0][3:]
    url = line.split("](")[1].split(")")[0]
    description = "" if line[-1] == ")" else line.split(") ")[1][2:]

    item: dict = {
        "name": name,
        "description": description,
        "url": url,
        "category": category,
    }

    if date:
        item["date"] = date

    return item


def parse_section(section: str, category: str = "", dated: bool = False) -> list[dict]:
    """Parse a section of lines into a list of structured items."""
    return [parse_line(line, category, dated) for line in section.split("\n") if line]


def parse_subsections(section: str, dated: bool = False) -> list[dict]:
    """Parse a section containing multiple subsections."""
    subsections = section.split("### ")[1:]

    items = []

    for subsection in subsections:
        split_section = subsection.split("\n\n")
        section_title = split_section[0]

        # Empty subsections use a "- None yet." placeholder so the Markdown stays well-formed.
        lines = [
            line
            for line in "\n\n".join(split_section[1:]).split("\n")
            if line.startswith(("- [", "– ["))
        ]

        items += parse_section("\n".join(lines), section_title, dated)

    return items


def cut_section(readme: str, start: str) -> str:
    """Extract a specific section from the README."""
    return readme.split(f"## {start}\n\n")[1].split("\n\n## ")[0]


def parse_readme(readme: str) -> dict:
    """Parse the entire README into a structured dictionary."""
    return {
        "apps": parse_subsections(cut_section(readme, "Apps")),
        "tools": parse_subsections(cut_section(readme, "Tools")),
        "resources": parse_subsections(cut_section(readme, "Resources"), dated=True),
        "sites": parse_section(cut_section(readme, "Open-source sites")),
        "metadata": {
            "updated": datetime.now(UTC).isoformat(),
        },
    }


if __name__ == "__main__":
    readme_path = Path("README.md")

    try:
        readme = readme_path.read_text(encoding="utf-8")
        parsed_readme = parse_readme(readme)

        json_path = Path(f"./dist{API_PATH}")
        json_path.parent.mkdir(parents=True, exist_ok=True)

        readme_payload = json.dumps(parsed_readme, indent=2, ensure_ascii=False)
        print(readme_payload)

        json_path.write_text(readme_payload, encoding="utf-8")

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        raise
    except (KeyError, IndexError) as e:
        print(f"Error: README formatting issue - {e}")
        print("Is the README well formatted?")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
