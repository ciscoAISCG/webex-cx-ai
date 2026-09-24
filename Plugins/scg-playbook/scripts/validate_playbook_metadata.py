"""Validate required metadata in every Playbooks/<folder>/README.md file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ALLOWED = {
    "Vertical": {
        "Education", "Energy Utilities", "Financial Services", "Government",
        "Health Care", "Hospitality Hotels And Leisure", "Manufacturing",
        "Media Entertainment", "Not For Profit", "Professional Services",
        "Retail", "Service Provider", "Technical Services", "Technology",
        "Transportation", "Wholesale Distribution", "Unknown",
    },
    "Channel": {
        "Voice", "Chat", "SMS", "Email", "Whatsapp", "RCS",
        "Apple Messages for Business", "Custom", "Unknown",
    },
    "Complexity": {"Beginner", "Intermediate", "Advanced", "Unknown"},
}

METADATA_SECTION = re.compile(
    r"^##\s+Playbook Metadata\s*$([\s\S]*?)(?=^##\s|\Z)", re.MULTILINE
)
TABLE_ROW = re.compile(r"^\|\s*(Vertical|Channel|Complexity)\s*\|\s*(.*?)\s*\|\s*$")


def read_metadata(readme: Path) -> dict[str, str]:
    text = readme.read_text(encoding="utf-8")
    section = METADATA_SECTION.search(text)
    if section is None:
        return {}
    values: dict[str, str] = {}
    for line in section.group(1).splitlines():
        match = TABLE_ROW.match(line.strip())
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


def validate(playbooks_root: Path) -> list[str]:
    errors: list[str] = []
    for folder in sorted(playbooks_root.iterdir(), key=lambda path: path.name.lower()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        readme = folder / "README.md"
        if not readme.exists():
            errors.append(f"{folder}: missing README.md")
            continue
        values = read_metadata(readme)
        for field, allowed in ALLOWED.items():
            value = values.get(field)
            if value is None:
                errors.append(f"{readme}: missing {field}")
            elif value not in allowed:
                errors.append(f"{readme}: invalid {field} value: {value}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("playbooks_root", nargs="?", default="Playbooks")
    args = parser.parse_args()
    errors = validate(Path(args.playbooks_root))
    if errors:
        print("Playbook metadata validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Playbook metadata validation passed: {args.playbooks_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
