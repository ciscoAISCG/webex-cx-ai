#!/usr/bin/env python3
"""Prove same-identity plugin replacement in an isolated Codex home."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


PLUGIN = "scg-update-lab"
MARKETPLACE = "ai-scg"
SELECTOR = f"{PLUGIN}@{MARKETPLACE}"
CURRENT_VERSION = "0.1.0+codex.lab-v2"
NEXT_VERSION = "0.1.0+codex.lab-v3"


def run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{detail}")
    return result


def assert_installed_version(
    codex_bin: str,
    env: dict[str, str],
    expected: str,
) -> str:
    output = run([codex_bin, "plugin", "list"], env).stdout
    matching_line = next(
        (line for line in output.splitlines() if line.split()[:1] == [SELECTOR]),
        None,
    )
    if matching_line is None:
        raise RuntimeError(f"{SELECTOR} was not listed after installation")
    if "installed, enabled" not in matching_line or expected not in matching_line:
        raise RuntimeError(
            f"Expected installed version {expected}, got: {matching_line}"
        )
    return output


def promote_disposable_copy_to_next_release(marketplace_root: Path) -> None:
    plugin_root = marketplace_root / "Plugins" / PLUGIN
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != CURRENT_VERSION:
        raise RuntimeError(
            f"Expected disposable source version {CURRENT_VERSION}"
        )
    manifest["version"] = NEXT_VERSION
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    skill_path = plugin_root / "skills" / PLUGIN / "SKILL.md"
    skill = skill_path.read_text(encoding="utf-8")
    skill = skill.replace("LAB_RELEASE=v2", "LAB_RELEASE=v3")
    skill = skill.replace(
        "LAB_MESSAGE=Marketplace update replacement is active.",
        "LAB_MESSAGE=Second marketplace update replacement is active.",
    )
    skill_path.write_text(skill, encoding="utf-8")


def assert_installed_skill_is_next_release(isolated_codex_home: Path) -> None:
    matching = [
        path
        for path in isolated_codex_home.rglob("SKILL.md")
        if path.parent.name == PLUGIN
        and "LAB_RELEASE=v3" in path.read_text(encoding="utf-8")
    ]
    if not matching:
        raise RuntimeError("Updated next-release skill content was not installed")


def main() -> int:
    codex_bin = shutil.which("codex")
    if codex_bin is None:
        raise RuntimeError("The Codex CLI was not found on PATH")

    plugin_root = Path(__file__).resolve().parents[1]
    repo_root = plugin_root.parents[1]
    catalog_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    if not catalog_path.is_file():
        raise RuntimeError("The repository marketplace catalog is missing")

    with tempfile.TemporaryDirectory(prefix="scg-plugin-update-lab-") as temp:
        temp_root = Path(temp)
        disposable_marketplace = temp_root / "marketplace"
        disposable_plugin = disposable_marketplace / "Plugins" / PLUGIN
        disposable_catalog = (
            disposable_marketplace / ".agents" / "plugins" / "marketplace.json"
        )
        isolated_home = temp_root / "home"
        isolated_codex_home = isolated_home / ".codex"

        shutil.copytree(plugin_root, disposable_plugin)
        disposable_catalog.parent.mkdir(parents=True)
        shutil.copy2(catalog_path, disposable_catalog)
        isolated_codex_home.mkdir(parents=True)

        env = os.environ.copy()
        env["HOME"] = str(isolated_home)
        env["CODEX_HOME"] = str(isolated_codex_home)

        print("1/6 Adding the disposable local marketplace")
        run(
            [
                codex_bin,
                "plugin",
                "marketplace",
                "add",
                str(disposable_marketplace),
            ],
            env,
        )

        print(f"2/6 Installing {CURRENT_VERSION}")
        run([codex_bin, "plugin", "add", SELECTOR], env)
        assert_installed_version(codex_bin, env, CURRENT_VERSION)

        print("3/6 Publishing the next release only in the disposable marketplace")
        promote_disposable_copy_to_next_release(disposable_marketplace)

        print(f"4/6 Reinstalling the same identity as {NEXT_VERSION}")
        run([codex_bin, "plugin", "add", SELECTOR], env)
        plugin_list = assert_installed_version(codex_bin, env, NEXT_VERSION)

        print("5/6 Confirming one identity and updated skill content")
        selector_count = len(
            re.findall(rf"(?m)^{re.escape(SELECTOR)}\s+", plugin_list)
        )
        if selector_count != 1:
            raise RuntimeError(
                f"Expected one installed identity, found {selector_count}"
            )
        assert_installed_skill_is_next_release(isolated_codex_home)

        print("6/6 Confirming production identities were never registered")
        if "scg-library@" in plugin_list or "scg-airtable@" in plugin_list:
            raise RuntimeError("A production plugin appeared in the isolated test home")

    print("\nPASS: the current release was replaced under one plugin identity.")
    print("PASS: the next-release skill content was installed.")
    print("PASS: no production SCG plugin was registered in the test home.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
