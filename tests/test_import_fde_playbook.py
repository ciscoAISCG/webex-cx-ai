from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from import_fde_playbook import (  # noqa: E402
    ImportFailure,
    import_playbook,
    load_changed_paths,
)


class ImportFdePlaybookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.source = self.root / "source"
        self.target = self.root / "target"
        (self.source / "Playbooks").mkdir(parents=True)
        (self.target / "Playbooks").mkdir(parents=True)
        (self.target / "Playbooks" / "taxonomy.yaml").write_text(
            "schema_version: 2\nfacets: {}\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def create_package(
        self,
        playbook_id: str = "example-playbook",
        *,
        security: dict[str, bool] | None = None,
        artifacts: dict[str, list[str]] | None = None,
    ) -> Path:
        package = self.source / "Playbooks" / playbook_id
        package.mkdir(parents=True)
        manifest = {
            "schema_version": 2,
            "id": playbook_id,
            "title": "Example playbook",
            "summary": "Example summary",
            "classification": {
                "features": ["ai-agent-autonomous-voice"],
                "customer_journeys": ["customer-service"],
            },
            "complexity": "beginner",
            "last_validated": "2026-09-29",
            "ownership": {"owner": "owner", "maintaining_team": "fde-team"},
            "validation": {
                "environment": "Test environment",
                "expected_result": "Expected result",
            },
            "security": security
            or {
                "customer_data_removed": True,
                "credentials_removed": True,
                "tenant_identifiers_removed": True,
            },
        }
        if artifacts is not None:
            manifest["artifacts"] = artifacts
        (package / "manifest.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
        )
        (package / "README.md").write_text("# Example\n", encoding="utf-8")
        return package

    def test_imports_declared_files_and_preserves_target_taxonomy(self) -> None:
        package = self.create_package(
            artifacts={"samples": ["samples/example.json"]}
        )
        (package / "samples").mkdir()
        (package / "samples" / "example.json").write_text(
            '{"safe": true}\n', encoding="utf-8"
        )
        old_target = self.target / "Playbooks" / "example-playbook"
        old_target.mkdir()
        (old_target / "obsolete.txt").write_text("obsolete\n", encoding="utf-8")
        taxonomy_before = (self.target / "Playbooks" / "taxonomy.yaml").read_text(
            encoding="utf-8"
        )

        playbook_id = import_playbook(
            self.source,
            self.target,
            [
                "Playbooks/example-playbook/README.md",
                "Playbooks/example-playbook/manifest.yaml",
                "Playbooks/example-playbook/samples/example.json",
            ],
        )

        self.assertEqual(playbook_id, "example-playbook")
        self.assertTrue((old_target / "README.md").is_file())
        self.assertTrue((old_target / "samples" / "example.json").is_file())
        self.assertFalse((old_target / "obsolete.txt").exists())
        self.assertEqual(
            (self.target / "Playbooks" / "taxonomy.yaml").read_text(
                encoding="utf-8"
            ),
            taxonomy_before,
        )

    def test_rejects_a_change_outside_the_playbook_package(self) -> None:
        self.create_package()
        with self.assertRaisesRegex(ImportFailure, "outside one playbook package"):
            import_playbook(
                self.source,
                self.target,
                [
                    "Playbooks/example-playbook/README.md",
                    "publication-process.md",
                ],
            )

    def test_rejects_multiple_playbooks(self) -> None:
        self.create_package("first-playbook")
        self.create_package("second-playbook")
        with self.assertRaisesRegex(ImportFailure, "exactly one changed playbook"):
            import_playbook(
                self.source,
                self.target,
                [
                    "Playbooks/first-playbook/README.md",
                    "Playbooks/second-playbook/README.md",
                ],
            )

    def test_rejects_false_security_attestation(self) -> None:
        self.create_package(
            security={
                "customer_data_removed": True,
                "credentials_removed": True,
                "tenant_identifiers_removed": False,
            }
        )
        with self.assertRaisesRegex(ImportFailure, "tenant_identifiers_removed"):
            import_playbook(
                self.source,
                self.target,
                ["Playbooks/example-playbook/manifest.yaml"],
            )

    def test_rejects_an_unlisted_file(self) -> None:
        package = self.create_package()
        (package / "secret.txt").write_text("not declared\n", encoding="utf-8")
        with self.assertRaisesRegex(ImportFailure, "unlisted files"):
            import_playbook(
                self.source,
                self.target,
                ["Playbooks/example-playbook/secret.txt"],
            )

    def test_rejects_artifact_path_traversal(self) -> None:
        self.create_package(artifacts={"samples": ["../outside.txt"]})
        with self.assertRaisesRegex(ImportFailure, "escapes the package"):
            import_playbook(
                self.source,
                self.target,
                ["Playbooks/example-playbook/manifest.yaml"],
            )

    def test_rejects_a_symbolic_link(self) -> None:
        package = self.create_package(artifacts={"samples": ["linked.txt"]})
        outside = self.root / "outside.txt"
        outside.write_text("outside\n", encoding="utf-8")
        (package / "linked.txt").symlink_to(outside)
        with self.assertRaisesRegex(ImportFailure, "symbolic links"):
            import_playbook(
                self.source,
                self.target,
                ["Playbooks/example-playbook/linked.txt"],
            )

    def test_loads_paginated_github_file_responses(self) -> None:
        response = self.root / "files.json"
        response.write_text(
            json.dumps(
                [
                    [{"filename": "Playbooks/example-playbook/README.md"}],
                    [{"filename": "Playbooks/example-playbook/manifest.yaml"}],
                ]
            ),
            encoding="utf-8",
        )
        self.assertEqual(
            load_changed_paths(response),
            [
                "Playbooks/example-playbook/README.md",
                "Playbooks/example-playbook/manifest.yaml",
            ],
        )


if __name__ == "__main__":
    unittest.main()
