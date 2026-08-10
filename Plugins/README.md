# Plugins

Installable packages distributed through the AI SCG Plugin Marketplace.

## Contributors: publish a marketplace plugin

Every marketplace contribution must be a plugin. A plugin may contain only one
skill, but it still requires this package structure:

```text
Plugins/<plugin-name>/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

- Keep the plugin folder name and manifest `name` identical and lower-case
  hyphenated.
- Give every plugin a valid semantic `version` in
  `.codex-plugin/plugin.json`.
- For a new plugin, add one entry to
  [the marketplace catalog](../.agents/plugins/marketplace.json).
- For an update, keep the same folder, plugin name, and catalog entry; update
  the contents and increase the manifest version. Do not create a numbered
  replacement folder.
- Validate the manifest and bundled skills, remove secrets and customer data,
  and submit the change through a feature branch and pull request.

Suggested Codex request:

> Package this skill as an AI SCG marketplace plugin named `<plugin-name>` and
> prepare a feature-branch pull request.

For a skill that does not need marketplace distribution, use the
[Skills contributor guide](../Skills/readme.md#contributors-build-a-standalone-skill).

## Available plugins

| Plugin | Status | Purpose |
| --- | --- | --- |
| [SCG Plugin Update Lab](./scg-update-lab/) | Experimental | Safely validates marketplace installation and same-identity updates in a disposable Codex environment. |
