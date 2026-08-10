# Plugins

Installable packages distributed through the AI SCG Plugin Marketplace.

## Contributors: start here

> [!IMPORTANT]
> **Copy and paste the prompt below into Codex.**
>
> Give Codex the skill, files, or capability you want to share first.

```text
Package or update this as an AI SCG marketplace plugin in ciscoAISCG/webex-cx-ai.
Read and follow the repository's AGENTS.md instructions. Ask me only for missing
product decisions, validate the package, and prepare a feature-branch pull
request. Do not merge it.
```

Codex should handle the package structure, manifest, marketplace registration,
versioning, validation, and GitHub workflow. The contributor only needs to
review and merge the pull request.

A plugin may contain only one skill. Codex will still create the required
installable package structure:

```text
Plugins/<plugin-name>/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

For updates, Codex must keep the same folder, manifest name, and
[marketplace entry](../.agents/plugins/marketplace.json). It updates the contents
and version rather than creating a numbered replacement plugin.

For a skill that does not need marketplace distribution, use the
[Skills contributor guide](../Skills/readme.md#contributors-start-here).

## Available plugins

| Plugin | Status | Purpose |
| --- | --- | --- |
| [SCG Plugin Update Lab](./scg-update-lab/) | Experimental | Safely validates marketplace installation and same-identity updates in a disposable Codex environment. |
