"""Validate schema-v2 metadata in every Playbooks/<folder>/manifest.yaml file."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml


def validate_values(
    manifest: dict[str, object], folder: Path, facets: dict[str, list[str]]
) -> list[str]:
    errors: list[str] = []
    manifest_path = folder / "manifest.yaml"

    if manifest.get("schema_version") != 2:
        errors.append(f"{manifest_path}: schema_version must be 2")
    if manifest.get("id") != folder.name:
        errors.append(f"{manifest_path}: id must match folder name ({folder.name})")

    for field in ("title", "summary"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            errors.append(f"{manifest_path}: missing or empty {field}")

    classification = manifest.get("classification")
    if not isinstance(classification, dict):
        classification = {}
        errors.append(f"{manifest_path}: missing classification mapping")

    for field in ("features", "customer_journeys"):
        values = classification.get(field)
        if not isinstance(values, list) or not values:
            errors.append(f"{manifest_path}: classification.{field} must be a non-empty list")
            continue
        allowed = facets.get(field, [])
        for value in values:
            if value not in allowed:
                errors.append(f"{manifest_path}: invalid classification.{field} value: {value}")

    for field in ("verticals", "channels", "integrations"):
        values = classification.get(field, [])
        if not isinstance(values, list):
            errors.append(f"{manifest_path}: classification.{field} must be a list")
            continue
        allowed = facets.get(field, [])
        for value in values:
            if value not in allowed:
                errors.append(f"{manifest_path}: invalid classification.{field} value: {value}")

    complexity = manifest.get("complexity")
    if complexity not in facets.get("complexity", []):
        errors.append(f"{manifest_path}: invalid or missing complexity: {complexity}")

    validated = manifest.get("last_validated")
    try:
        if not isinstance(validated, str) or date.fromisoformat(validated).isoformat() != validated:
            raise ValueError
    except ValueError:
        errors.append(f"{manifest_path}: last_validated must use YYYY-MM-DD format")

    ownership = manifest.get("ownership")
    if not isinstance(ownership, dict):
        ownership = {}
    for field in ("owner", "maintaining_team"):
        if not isinstance(ownership.get(field), str) or not ownership[field].strip():
            errors.append(f"{manifest_path}: missing or empty ownership.{field}")

    return errors


def validate(playbooks_root: Path) -> list[str]:
    errors: list[str] = []
    taxonomy_path = playbooks_root / "taxonomy.yaml"
    try:
        taxonomy = yaml.safe_load(taxonomy_path.read_text(encoding="utf-8"))
        facets = taxonomy["facets"]
        if not isinstance(facets, dict):
            raise ValueError("facets must be a mapping")
    except (OSError, KeyError, TypeError, yaml.YAMLError, ValueError) as exc:
        return [f"{taxonomy_path}: could not load taxonomy facets: {exc}"]

    for folder in sorted(playbooks_root.iterdir(), key=lambda path: path.name.lower()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        readme = folder / "README.md"
        if not readme.exists():
            errors.append(f"{folder}: missing README.md")
            continue
        manifest_path = folder / "manifest.yaml"
        try:
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"{manifest_path}: could not load manifest: {exc}")
            continue
        if not isinstance(manifest, dict):
            errors.append(f"{manifest_path}: manifest must be a mapping")
            continue
        errors.extend(validate_values(manifest, folder, facets))
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
    print(f"Playbook manifest validation passed: {args.playbooks_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
