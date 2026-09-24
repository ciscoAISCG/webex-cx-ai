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

- README links resolve or are clearly marked as placeholders.
- Recommended path is visible without expanding sections.
- Advanced details are collapsed.
- Skills Shed links point to the target repo path and did not create local folders.
- No full real names, secrets, tokens, or private tenant IDs appear in customer-facing prose.
- The playbook says which parts must be rebound after import.
- The `Files In This Playbook` section, when present, does not list hero diagrams, architecture diagrams, screenshots, SVGs, PNGs, or other files from `assets/`.
- Simple visuals have no arrows, labels, connectors, or decorative shapes overlapping text, cards, icons, or each other.
- Arrow labels are in separate pill callouts and not placed directly on connector lines.
- A teammate can understand the first successful test in about five minutes.

## Useful Searches

```bash
rg -n "token|secret|password|bearer|api[_-]?key|orgId|tenant|queue|@|\\+1" Playbooks/<Playbook_Folder>
```

Review the matches manually. Some words, like `token` or `queue`, may be legitimate when described generically.
