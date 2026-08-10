#!/usr/bin/env python3
"""Validate AI SCG standalone skills and marketplace plugin packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
REQUIRED_INTERFACE_FIELDS = (
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
)
REQUIRED_INSTRUCTION_FILES = (
    "AGENTS.md",
    "Plugins/AGENTS.md",
    "Skills/AGENTS.md",
)


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing required file: {path}")
        return None
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"Expected a JSON object in {path}")
        return None
    return value


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _resolve_relative(
    owner: Path, raw_path: Any, label: str, errors: list[str]
) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path.startswith("./"):
        errors.append(f"{label} must be a relative path beginning with './'")
        return None
    resolved_owner = owner.resolve()
    resolved = (owner / raw_path[2:]).resolve()
    try:
        resolved.relative_to(resolved_owner)
    except ValueError:
        errors.append(f"{label} escapes its package root: {raw_path}")
        return None
    return resolved


def _frontmatter(skill_file: Path, errors: list[str]) -> dict[str, str] | None:
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        errors.append(f"Missing skill file: {skill_file}")
        return None
    if not lines or lines[0].strip() != "---":
        errors.append(f"Missing YAML frontmatter in {skill_file}")
        return None
    try:
        closing = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        errors.append(f"Unclosed YAML frontmatter in {skill_file}")
        return None

    values: dict[str, str] = {}
    for line in lines[1:closing]:
        match = re.match(r"^(name|description):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("'\"")

    name = values.get("name", "")
    description = values.get("description", "")
    if not name:
        errors.append(f"Missing frontmatter name in {skill_file}")
    elif not NAME_PATTERN.fullmatch(name):
        errors.append(f"Invalid skill name '{name}' in {skill_file}")
    if not description:
        errors.append(f"Missing frontmatter description in {skill_file}")
    return values


def _validate_plugin(
    repo_root: Path,
    entry: dict[str, Any],
    errors: list[str],
) -> tuple[str | None, Path | None]:
    name = entry.get("name")
    if not _nonempty_string(name) or not NAME_PATTERN.fullmatch(name):
        errors.append(f"Marketplace plugin has invalid name: {name!r}")
        return None, None

    source = entry.get("source")
    if not isinstance(source, dict) or source.get("source") != "local":
        errors.append(f"Marketplace plugin '{name}' must use a local source")
        return name, None
    raw_path = source.get("path")
    if not isinstance(raw_path, str) or not raw_path.startswith("./Plugins/"):
        errors.append(
            f"Marketplace plugin '{name}' source must begin with './Plugins/'"
        )
        return name, None
    plugin_dir = _resolve_relative(repo_root, raw_path, f"Plugin '{name}' source", errors)
    if plugin_dir is None:
        return name, None
    if not plugin_dir.is_dir():
        errors.append(f"Marketplace plugin '{name}' folder does not exist: {raw_path}")
        return name, plugin_dir
    if plugin_dir.name != name:
        errors.append(
            f"Marketplace name '{name}' does not match folder '{plugin_dir.name}'"
        )

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append(f"Marketplace plugin '{name}' is missing policy metadata")
    else:
        if policy.get("installation") not in {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}:
            errors.append(f"Marketplace plugin '{name}' has invalid installation policy")
        if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
            errors.append(f"Marketplace plugin '{name}' has invalid authentication policy")
    if not _nonempty_string(entry.get("category")):
        errors.append(f"Marketplace plugin '{name}' is missing category")

    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    manifest = _read_json(manifest_path, errors)
    if manifest is None:
        return name, plugin_dir

    plugin_readme = plugin_dir / "README.md"
    if not plugin_readme.is_file():
        errors.append(f"Plugin '{name}' is missing README.md")
    elif "../README.md#consumers-check-for-updates" not in plugin_readme.read_text(
        encoding="utf-8"
    ):
        errors.append(
            f"Plugin '{name}' README.md must link to the canonical update instructions"
        )

    if manifest.get("name") != name:
        errors.append(f"Manifest name in {manifest_path} must be '{name}'")
    version = manifest.get("version")
    if not _nonempty_string(version) or not SEMVER_PATTERN.fullmatch(version):
        errors.append(f"Manifest {manifest_path} has invalid semantic version: {version!r}")
    if not _nonempty_string(manifest.get("description")):
        errors.append(f"Manifest {manifest_path} is missing description")
    author = manifest.get("author")
    if not isinstance(author, dict) or not _nonempty_string(author.get("name")):
        errors.append(f"Manifest {manifest_path} is missing author.name")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"Manifest {manifest_path} is missing interface metadata")
    else:
        for field in REQUIRED_INTERFACE_FIELDS:
            if not _nonempty_string(interface.get(field)):
                errors.append(f"Manifest {manifest_path} is missing interface.{field}")
        if interface.get("category") != entry.get("category"):
            errors.append(
                f"Plugin '{name}' category must match in manifest and marketplace"
            )

    components = 0
    if "skills" in manifest:
        components += 1
        skills_dir = _resolve_relative(
            plugin_dir, manifest.get("skills"), f"Plugin '{name}' skills path", errors
        )
        if skills_dir is not None:
            if not skills_dir.is_dir():
                errors.append(f"Plugin '{name}' skills folder does not exist")
            else:
                skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
                if not skill_dirs:
                    errors.append(f"Plugin '{name}' declares skills but contains none")
                for skill_dir in skill_dirs:
                    values = _frontmatter(skill_dir / "SKILL.md", errors)
                    if values and values.get("name") != skill_dir.name:
                        errors.append(
                            f"Skill name in {skill_dir / 'SKILL.md'} must match folder '{skill_dir.name}'"
                        )

    mcp_servers = manifest.get("mcpServers")
    if mcp_servers is not None:
        components += 1
        if isinstance(mcp_servers, str):
            mcp_path = _resolve_relative(
                plugin_dir, mcp_servers, f"Plugin '{name}' MCP path", errors
            )
            if mcp_path is not None and not mcp_path.is_file():
                errors.append(f"Plugin '{name}' MCP configuration does not exist")
        elif not isinstance(mcp_servers, dict):
            errors.append(f"Plugin '{name}' mcpServers must be a path or object")

    if "apps" in manifest:
        components += 1
        app_path = _resolve_relative(
            plugin_dir, manifest.get("apps"), f"Plugin '{name}' app path", errors
        )
        if app_path is not None and not app_path.is_file():
            errors.append(f"Plugin '{name}' app manifest does not exist")

    if components == 0:
        errors.append(f"Plugin '{name}' must declare skills, mcpServers, or apps")
    return name, plugin_dir


def validate_repository(repo_root: Path) -> tuple[list[str], int, int]:
    repo_root = repo_root.resolve()
    errors: list[str] = []
    for relative_path in REQUIRED_INSTRUCTION_FILES:
        instruction_path = repo_root / relative_path
        if not instruction_path.is_file():
            errors.append(f"Missing required Codex instructions: {relative_path}")
        elif not instruction_path.read_text(encoding="utf-8").strip():
            errors.append(f"Codex instructions must not be empty: {relative_path}")

    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    marketplace = _read_json(marketplace_path, errors)
    plugin_names: set[str] = set()
    plugin_paths: set[Path] = set()

    if marketplace is not None:
        if marketplace.get("name") != "ai-scg":
            errors.append("Marketplace name must remain 'ai-scg'")
        entries = marketplace.get("plugins")
        if not isinstance(entries, list):
            errors.append(f"Expected a plugins array in {marketplace_path}")
        else:
            for entry in entries:
                if not isinstance(entry, dict):
                    errors.append("Every marketplace plugin entry must be an object")
                    continue
                name, plugin_dir = _validate_plugin(repo_root, entry, errors)
                if name:
                    if name in plugin_names:
                        errors.append(f"Duplicate marketplace plugin name: {name}")
                    plugin_names.add(name)
                if plugin_dir:
                    if plugin_dir in plugin_paths:
                        errors.append(f"Duplicate marketplace plugin path: {plugin_dir}")
                    plugin_paths.add(plugin_dir)

    plugins_root = repo_root / "Plugins"
    actual_plugin_dirs = {
        path.resolve()
        for path in plugins_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    } if plugins_root.is_dir() else set()
    for unlisted in sorted(actual_plugin_dirs - plugin_paths):
        errors.append(f"Plugin folder is missing from marketplace: {unlisted.relative_to(repo_root)}")

    standalone_count = 0
    skills_root = repo_root / "Skills"
    if skills_root.is_dir():
        for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
            standalone_count += 1
            _frontmatter(skill_dir / "SKILL.md", errors)

    return errors, len(plugin_names), standalone_count


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    errors, plugin_count, skill_count = validate_repository(repo_root)
    if errors:
        print("SCG contribution validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "SCG contribution validation passed: "
        f"{plugin_count} marketplace plugin(s), {skill_count} standalone skill(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
