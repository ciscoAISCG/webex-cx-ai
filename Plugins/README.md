# Plugins

Installable packages distributed through the AI SCG Plugin Marketplace.

## Consumers: check for updates

> [!IMPORTANT]
> **Copy and paste the prompt below into Codex.**
>
> This checks only AI SCG plugins you already installed. It does not install
> new plugins.

```text
Check my installed AI SCG marketplace plugins for updates. Refresh the ai-scg
marketplace first. Update only plugins I already have installed; do not install
any new plugins. Report what changed and tell me whether I need to start a new
task to load the updates.
```

Skills packaged inside a plugin update with that plugin. If nothing has
changed, Codex should report that all installed AI SCG plugins are up to date.

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
| [SCG Library](./scg-library/) | Available | Securely queries the read-only SCG business-data library with Auth0 identity verification, Cisco-domain auto-approval, and administrator-controlled external access. |
