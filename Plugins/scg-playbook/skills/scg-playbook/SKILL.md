---
name: scg-playbook
description: Create SCG-style, visual-first Webex CX AI Agent and Contact Center playbooks from AI Agent Studio exports, Flow Designer exports, Webex Connect or MCP setup notes, screenshots, and rough field notes. Use when AI SCG team members need a reusable Playbooks/playbook-folder package that is easy to adopt, with Try It Fast steps, SCG visuals, rounded Mermaid diagrams, Skills helper links, collapsible advanced details, customer/internal cleanup, validation, and GitHub-ready packaging.
metadata:
  short-description: Create visual-first SCG playbooks
---

# SCG Playbook

Use this skill to turn a working Webex CX AI Agent, voice flow, digital fulfillment path, MCP integration, or field-built demo into a playbook that people will actually try.

The playbook should feel like a guided starter kit, not a long manual. Lead with the recommended path, make the first win visible, and collapse advanced or optional material.

## First Move

1. Identify the audience: `internal`, `customer`, or `both`.
2. Ask for or inventory these downloadable content-file categories:
   - Webex Contact Center Voice Flows
   - Webex Contact Center Fulfilment Flows
   - Webex Connect Fulfilment Flows
   - AI Agent Export JSON
   - Sample Knowledge Base Files
   Store supplied originals unchanged under `content/` or `downloads/`. Treat them as downloadable package content only: do not inspect, summarize, transform, or use them to generate the README, diagrams, prompts, or other playbook content unless the user explicitly authorizes a named file or category.
3. If the user explicitly authorizes using an AI Agent Studio or Flow Designer JSON as a source, inspect it with `scripts/inspect_playbook.py`. Otherwise, preserve it as downloadable content only.
4. Choose one recommended setup path. Put alternatives in collapsed sections.
5. For any simple visual or hero image, load `references/visual-standard.md` and apply the arrow-safety rules before delivering the asset.
6. Capture the required playbook metadata in the README using the controlled values below. Use `Unknown` when the value is not known.
7. Build or refresh `Playbooks/<Playbook_Folder>/` with README, exports, content files, and assets.
8. Add a `Downloadable Content Files` section to the README that accounts for all five categories and links every supplied original file.
9. Validate before calling it done: metadata, downloadable content links, JSON, SVG/assets, links, security cleanup, import notes, and visual overlap checks.

## SCG Playbook Shape

Every playbook should include:

- A short title and one plain-language promise.
- A `Playbook Metadata` section with exactly one value for each required field:
  - `Vertical`: `Education`, `Energy Utilities`, `Financial Services`, `Government`, `Health Care`, `Hospitality Hotels And Leisure`, `Manufacturing`, `Media Entertainment`, `Not For Profit`, `Professional Services`, `Retail`, `Service Provider`, `Technical Services`, `Technology`, `Transportation`, `Wholesale Distribution`, or `Unknown`.
  - `Channel`: `Voice`, `Chat`, `SMS`, `Email`, `Whatsapp`, `RCS`, `Apple Messages for Business`, `Custom`, or `Unknown`.
  - `Complexity`: `Beginner`, `Intermediate`, `Advanced`, or `Unknown`.
- A friendly hero visual that explains the use case at a glance and has no arrows or labels crossing text.
- A `Downloadable Content Files` section listing the five requested categories and relative download links for every supplied file. Mark a category `Not provided` when no file was supplied.
- `Try It Fast`: the shortest successful setup path.
- A setup checklist with the recommended path visible.
- A test script that lets the reader prove the use case works.
- Collapsed advanced sections for architecture, export details, backend paths, security, limits, and publishing notes.
- A Skills call-to-action when another skill reduces setup confusion.
- If the README includes a `Files In This Playbook` section, list only files or dependencies needed to run, import, or configure the playbook. Do not list diagrams, hero visuals, screenshots, or other files from `assets/` in that section.

If the playbook starts to read like a reference document, move the detail into `<details>` sections or a separate file.

Use this exact README block for the metadata:

```markdown
## Playbook Metadata

| Field | Value |
|---|---|
| Vertical | Unknown |
| Channel | Unknown |
| Complexity | Unknown |
```

Use this structure for the downloadable content index. Replace each placeholder with one or more relative links to the unchanged files under `content/` or `downloads/`; use `Not provided` when a category was not supplied.

```markdown
## Downloadable Content Files

These files are included for download and reference. They were not used to generate this playbook unless explicitly authorized by the user.

| Category | Files |
|---|---|
| Webex Contact Center Voice Flows | Not provided |
| Webex Contact Center Fulfilment Flows | Not provided |
| Webex Connect Fulfilment Flows | Not provided |
| AI Agent Export JSON | Not provided |
| Sample Knowledge Base Files | Not provided |
```

## Reference Guide

Load only the reference needed for the current task:

- `references/playbook-style.md`: README order, tone, collapsed sections, and adoption-first writing.
- `references/visual-standard.md`: SCG hero visuals, arrow-safe simple visuals, rounded Mermaid diagrams, and screenshot/asset rules.
- `references/skill-shed-links.md`: how to link to helper skills without creating local Skills folders.
- `references/customer-cleanup.md`: names, secrets, tenant data, demo credentials, and customer-safe cleanup.
- `references/validation-checklist.md`: commands and checks before delivery.
- `references/github-packaging.md`: GitHub repo packaging expectations and PR flow.

## Output Modes

- `draft`: create the playbook quickly from available artifacts, with assumptions clearly marked.
- `refresh`: update an existing playbook while preserving its style and importable exports.
- `publish-ready`: perform cleanup, validation, index guidance, and GitHub handoff notes.

Ask which mode only if it materially changes the work. Otherwise, choose `draft` for new ideas and `publish-ready` when the user asks to distribute.

## Guardrails

- Do not create a local `Skills/` folder in the `one_drive` skill-source project. Skills is a target folder in the shared GitHub repo unless the user explicitly says otherwise.
- Keep root-level skill folders as the source of truth in `one_drive`; `/Users/ntheolog/.codex/skills/<skill-name>/` is only the installed testing copy.
- Do not expose full real names, real customer data, secrets, API tokens, bearer tokens, private tenant IDs, org IDs, or production phone numbers in customer-facing playbooks.
- Preserve importability of JSON exports unless the user explicitly asks to sanitize the export itself. If sanitizing may break import, say so.
- Prefer one recommended path over equal-weight options. Collapsing options is usually better than making the reader choose too early.
- Do not deliver generated visuals where arrows, labels, connectors, or decorative shapes overlap text, cards, icons, or each other. Iterate or simplify the visual first.
- Keep diagrams and visual assets in the repo when useful, usually under `assets/`, but do not add them to the README's `Files In This Playbook` section or table.
- Use official Webex documentation links when referencing platform setup, and verify time-sensitive docs if the exact UI or feature support matters.
