#!/usr/bin/env python3
"""Tests for the AI SCG contribution validator."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_contributions import validate_repository


class ContributionValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self._write("AGENTS.md", "# Repository instructions\n")
        self._write("Plugins/AGENTS.md", "# Plugin instructions\n")
        self._write("Skills/AGENTS.md", "# Skill instructions\n")
        self._write(
            ".agents/plugins/marketplace.json",
            json.dumps(
                {
                    "name": "ai-scg",
                    "interface": {"displayName": "AI SCG Plugin Marketplace"},
                    "plugins": [
                        {
                            "name": "example-plugin",
                            "source": {
                                "source": "local",
                                "path": "./Plugins/example-plugin",
                            },
                            "policy": {
                                "installation": "AVAILABLE",
                                "authentication": "ON_INSTALL",
                            },
                            "category": "Productivity",
                        }
                    ],
                }
            ),
        )
        self._write(
            "Plugins/example-plugin/.codex-plugin/plugin.json",
            json.dumps(
                {
                    "name": "example-plugin",
                    "version": "1.0.0",
                    "description": "Example plugin",
                    "author": {"name": "AI SCG"},
                    "skills": "./skills/",
                    "interface": {
                        "displayName": "Example Plugin",
                        "shortDescription": "Example plugin",
                        "longDescription": "Example marketplace plugin",
                        "developerName": "AI SCG",
                        "category": "Productivity",
                    },
                }
            ),
        )
        self._write(
            "Plugins/example-plugin/README.md",
            "## Installation\n\nAsk for Approval.\n\n"
            "```text\nInstall example-plugin.\n```\n\n"
            "## Updates\n\n"
            "[Update instructions](../README.md#update-my-plugins)\n",
        )
        self._write(
            "Plugins/example-plugin/skills/example-skill/SKILL.md",
            "---\nname: example-skill\ndescription: Example skill.\n---\n",
        )
        self._write(
            "Skills/standalone-skill/SKILL.md",
            "---\nname: standalone-skill\ndescription: Standalone example.\n---\n",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_valid_repository(self) -> None:
        errors, plugin_count, skill_count = validate_repository(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(plugin_count, 1)
        self.assertEqual(skill_count, 1)

    def test_missing_manifest_is_rejected(self) -> None:
        (self.root / "Plugins/example-plugin/.codex-plugin/plugin.json").unlink()
        errors, _, _ = validate_repository(self.root)
        self.assertTrue(any("Missing required file" in error for error in errors))

    def test_missing_scoped_instructions_are_rejected(self) -> None:
        (self.root / "Plugins/AGENTS.md").unlink()
        errors, _, _ = validate_repository(self.root)
        self.assertTrue(any("Missing required Codex instructions" in error for error in errors))

    def test_invalid_version_is_rejected(self) -> None:
        manifest_path = self.root / "Plugins/example-plugin/.codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["version"] = "version-two"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        errors, _, _ = validate_repository(self.root)
        self.assertTrue(any("invalid semantic version" in error for error in errors))

    def test_missing_update_link_is_rejected(self) -> None:
        readme_path = self.root / "Plugins/example-plugin/README.md"
        readme_path.write_text("# Example plugin\n", encoding="utf-8")
        errors, _, _ = validate_repository(self.root)
        self.assertTrue(any("canonical update instructions" in error for error in errors))

    def test_missing_natural_language_installation_is_rejected(self) -> None:
        readme_path = self.root / "Plugins/example-plugin/README.md"
        readme_path.write_text(
            "## Installation\n\nRun a terminal command.\n\n"
            "[Update instructions](../README.md#update-my-plugins)\n",
            encoding="utf-8",
        )
        errors, _, _ = validate_repository(self.root)
        self.assertTrue(any("natural-language Installation prompt" in error for error in errors))

    def test_missing_approval_prerequisite_is_rejected(self) -> None:
        readme_path = self.root / "Plugins/example-plugin/README.md"
        readme_path.write_text(
            "## Installation\n\n```text\nInstall example-plugin.\n```\n\n"
            "[Update instructions](../README.md#update-my-plugins)\n",
            encoding="utf-8",
        )
        errors, _, _ = validate_repository(self.root)
        self.assertTrue(any("Ask for Approval prerequisite" in error for error in errors))

    def test_unlisted_plugin_folder_is_rejected(self) -> None:
        self._write(
            "Plugins/unlisted/.codex-plugin/plugin.json",
            json.dumps({"name": "unlisted"}),
        )
        errors, _, _ = validate_repository(self.root)
        self.assertTrue(any("missing from marketplace" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
