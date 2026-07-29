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
V1 = "0.1.0+codex.lab-v1"
V2 = "0.1.0+codex.lab-v2"


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


def promote_disposable_copy_to_v2(marketplace_root: Path) -> None:
    plugin_root = marketplace_root / "Plugins" / PLUGIN
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != V1:
        raise RuntimeError(f"Expected disposable source version {V1}")
    manifest["version"] = V2
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    skill_path = plugin_root / "skills" / PLUGIN / "SKILL.md"
    skill = skill_path.read_text(encoding="utf-8")
    skill = skill.replace("LAB_RELEASE=v1", "LAB_RELEASE=v2")
    skill = skill.replace(
        "LAB_MESSAGE=Initial marketplace installation is active.",
        "LAB_MESSAGE=Marketplace update replacement is active.",
    )
    skill_path.write_text(skill, encoding="utf-8")


def assert_installed_skill_is_v2(isolated_codex_home: Path) -> None:
    matching = [
        path
        for path in isolated_codex_home.rglob("SKILL.md")
        if path.parent.name == PLUGIN
        and "LAB_RELEASE=v2" in path.read_text(encoding="utf-8")
    ]
    if not matching:
        raise RuntimeError("Updated v2 skill content was not installed")


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

        print(f"2/6 Installing {V1}")
        run([codex_bin, "plugin", "add", SELECTOR], env)
        assert_installed_version(codex_bin, env, V1)

        print("3/6 Publishing v2 only into the disposable marketplace")
        promote_disposable_copy_to_v2(disposable_marketplace)

        print(f"4/6 Reinstalling the same identity as {V2}")
        run([codex_bin, "plugin", "add", SELECTOR], env)
        plugin_list = assert_installed_version(codex_bin, env, V2)

        print("5/6 Confirming one identity and updated skill content")
        selector_count = len(
            re.findall(rf"(?m)^{re.escape(SELECTOR)}\s+", plugin_list)
        )
        if selector_count != 1:
            raise RuntimeError(
                f"Expected one installed identity, found {selector_count}"
            )
        assert_installed_skill_is_v2(isolated_codex_home)

        print("6/6 Confirming production identities were never registered")
        if "scg-library@" in plugin_list or "scg-airtable@" in plugin_list:
            raise RuntimeError("A production plugin appeared in the isolated test home")

    print("\nPASS: v1 was replaced by v2 under one lab plugin identity.")
    print("PASS: the updated v2 skill content was installed.")
    print("PASS: no production SCG plugin was registered in the test home.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
