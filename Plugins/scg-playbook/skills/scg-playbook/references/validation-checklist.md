# Validation Checklist

Run the smallest checks that give confidence the playbook is usable.

## Core Checks

```bash
jq empty Playbooks/<playbook-id>/*.json
python3 Plugins/scg-playbook/scripts/inspect_playbook.py Playbooks/<playbook-id>
xmllint --noout Playbooks/<playbook-id>/assets/*.svg
python3 Plugins/scg-playbook/scripts/validate_playbook_metadata.py Playbooks
python3 scripts/generate_playbook_catalog.py
```

If no SVG exists, validate the image format another way or open it visually.

## Content Checks

- Each playbook folder uses lowercase kebab-case and contains both `manifest.yaml` and `README.md`.
- `manifest.yaml` uses schema version 2, its `id` matches the folder name, and all classifications use values from `Playbooks/taxonomy.yaml`.
- Required manifest fields are present: `id`, `date_added`, `title`, `summary`, non-empty `classification.features`, non-empty `classification.customer_journeys`, `complexity`, `last_validated`, `ownership.owner`, and `ownership.maintaining_team`.
- `date_added` records when the playbook first entered this repository and uses `YYYY-MM-DD` format; indexes display the newest playbooks first.
- Optional `classification.verticals`, `classification.channels`, and `classification.integrations` contain only allowed taxonomy values when present.
- README does not duplicate manifest classifications or complexity in a `Playbook Metadata` table.
- README has a `Watch Me` / `Try Me` / `Get Me` action row immediately after its title. `Watch Me` and `Try Me` use supplied optional URLs or say `link not provided`; `Get Me` links to `exports/`, and that folder exists in the package.
- README contains a `Downloadable Content Files` section covering Webex Contact Center Voice Flows, Webex Contact Center Fulfilment Flows, Webex Connect Fulfilment Flows, AI Agent Export JSON, and Sample Knowledge Base Files.
- Every supplied content file is preserved unchanged under `content/` or `downloads/` and linked with a relative download link; categories without supplied files are marked `Not provided`.
- The README clearly says downloadable content files were not used to generate playbook content unless the user explicitly authorized it.
- README links resolve or are clearly marked as placeholders.
- `Playbooks/README.md` and `Cookbooks/docs/playbooks.md` are regenerated from manifests with `python3 scripts/generate_playbook_catalog.py`; do not edit generated catalog files by hand.
- Recommended path is visible without expanding sections.
- Advanced details are collapsed.
- Skills links point to the target repo path and did not create local folders.
- No full real names, secrets, tokens, or private tenant IDs appear in customer-facing prose.
- The playbook says which parts must be rebound after import.
- The `Files In This Playbook` section, when present, does not list hero diagrams, architecture diagrams, screenshots, SVGs, PNGs, or other files from `assets/`.
- Downloadable-only content files are listed in `Downloadable Content Files`, not `Files In This Playbook`, unless they are required to run, import, or configure the playbook.
- Simple visuals have no arrows, labels, connectors, or decorative shapes overlapping text, cards, icons, or each other.
- Arrow labels are in separate pill callouts and not placed directly on connector lines.
- A teammate can understand the first successful test in about five minutes.

## Useful Searches

```bash
rg -n "token|secret|password|bearer|api[_-]?key|orgId|tenant|queue|@|\\+1" Playbooks/<playbook-id>
```

Review the matches manually. Some words, like `token` or `queue`, may be legitimate when described generically.

For repository-wide schema-v2 manifest validation, run this from the repository root:

```bash
python3 Plugins/scg-playbook/scripts/validate_playbook_metadata.py Playbooks
```
