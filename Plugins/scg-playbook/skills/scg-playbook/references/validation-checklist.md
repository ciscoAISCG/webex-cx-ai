# Validation Checklist

Run the smallest checks that give confidence the playbook is usable.

## Core Checks

```bash
jq empty Playbooks/<Playbook_Folder>/*.json
python3 scg-playbook/scripts/inspect_playbook.py Playbooks/<Playbook_Folder>
xmllint --noout Playbooks/<Playbook_Folder>/assets/*.svg
```

If no SVG exists, validate the image format another way or open it visually.

## Content Checks

- README contains a `Playbook Metadata` table with `Vertical`, `Channel`, and `Complexity`.
- Metadata values match the controlled lists in `SKILL.md`; use `Unknown` when a value is not known.
- README contains a `Downloadable Content Files` section covering Webex Contact Center Voice Flows, Webex Contact Center Fulfilment Flows, Webex Connect Fulfilment Flows, AI Agent Export JSON, and Sample Knowledge Base Files.
- Every supplied content file is preserved unchanged under `content/` or `downloads/` and linked with a relative download link; categories without supplied files are marked `Not provided`.
- The README clearly says downloadable content files were not used to generate playbook content unless the user explicitly authorized it.
- README links resolve or are clearly marked as placeholders.
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
rg -n "token|secret|password|bearer|api[_-]?key|orgId|tenant|queue|@|\\+1" Playbooks/<Playbook_Folder>
```

Review the matches manually. Some words, like `token` or `queue`, may be legitimate when described generically.

For repository-wide metadata validation, run:

```bash
python scripts/validate_playbook_metadata.py Playbooks
```
