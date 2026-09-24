# GitHub Packaging

Use this when the playbook is headed to the shared `ciscoAISCG/webex-cx-ai` repo.

## Target Structure

```text
Playbooks/<Playbook_Folder>/
  README.md
  <ai-agent-export>.json
  <flow-designer-export>.json
  assets/
    <hero-or-diagram>.svg
```

Optional files are fine when needed, but keep the first-run path obvious.

Keep useful diagrams and images in `assets/`, but do not list those visual assets in the README's `Files In This Playbook` section. That section is for importable/configuration-critical playbook files and required dependencies, not supporting visuals.

## Skills

Helper skills belong in the shared repo's `Skills/<skill-name>/` folder when publishing there. Do not create that folder in the local `one_drive` skill-source project unless the user has checked out the target repo and asks for it.

## Publishing Flow

1. Use `scg-github` for branch, commit, push, and PR guidance.
2. Update the Playbooks index when the repo has one.
3. Keep PR notes short: use case, included artifacts, validation performed, and known limitations.
4. Call out whether the playbook is internal-only, customer-safe, or hybrid.
