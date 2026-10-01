# GitHub Packaging

Use this when the playbook is headed to the shared `ciscoAISCG/webex-cx-ai` repo.

## Target Structure

```text
Playbooks/
  taxonomy.yaml                 # shared repository taxonomy; do not copy into each package
  <playbook-id>/                 # lowercase kebab-case, e.g. concierge-ai-agent
    manifest.yaml                # schema_version: 2; id must match <playbook-id>
    README.md
    content/                     # optional original downloadable source files
    downloads/                   # optional original downloadable source files
    <ai-agent-export>.json
    <flow-designer-export>.json
    assets/
      <hero-or-diagram>.svg
```

Optional files are fine when needed, but keep the first-run path obvious. The `manifest.yaml` is required; follow schema version 2 and the facets in `Playbooks/taxonomy.yaml`. Do not add a duplicate Playbook Metadata table to the README.

Keep useful diagrams and images in `assets/`, but do not list those visual assets in the README's `Files In This Playbook` section. That section is for importable/configuration-critical playbook files and required dependencies, not supporting visuals.

## Skills

Helper skills belong in the shared repo's `Skills/<skill-name>/` folder when publishing there. Do not create that folder in the local `one_drive` skill-source project unless the user has checked out the target repo and asks for it.

## Publishing Flow

1. Use `scg-github` for branch, commit, push, and PR guidance.
2. Update `Playbooks/<playbook-id>/manifest.yaml`, then run `python3 scripts/generate_playbook_catalog.py` from the repository root. This regenerates both `Playbooks/README.md` and `Cookbooks/docs/playbooks.md`; do not edit those generated indexes by hand.
3. Keep PR notes short: use case, included artifacts, validation performed, and known limitations.
4. Call out whether the playbook is internal-only, customer-safe, or hybrid.
