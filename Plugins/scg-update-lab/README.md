# SCG Plugin Update Lab

This non-production plugin proves the AI SCG marketplace installation and
update workflow without modifying any working SCG skill, plugin, MCP server, or
configuration.

## Installation

> [!IMPORTANT]
> **Copy and paste the prompt below into Codex.**

```text
Install scg-update-lab from the AI SCG marketplace in
ciscoAISCG/webex-cx-ai using branch main. Do not ask me to run terminal
commands; perform the plugin-management steps yourself. If the ai-scg
marketplace is not configured, add it. Install only scg-update-lab, verify its
source and installed version, and tell me when to start a new Codex task.
```

## Isolation guarantees

- Unique plugin identity: `scg-update-lab`
- Marketplace identity: `ai-scg`
- No MCP server, app, hook, authentication, or Airtable configuration
- No customer or production data
- Automated tests use a temporary `HOME` and `CODEX_HOME`
- The test publishes the next release only into a disposable copy of this plugin

## Run the isolated test

From the repository root:

```bash
python3 Plugins/scg-update-lab/scripts/test_isolated_update.py
```

The script copies only this lab and the marketplace catalog into a temporary
directory. It installs the currently published release, changes the disposable
copy to the next release, reinstalls the same identity, and verifies that only
one lab plugin is present.

Do not add working SCG plugins or production connections to this lab.

## Updates

Use the canonical [AI SCG marketplace update instructions](../README.md#consumers-check-for-updates).
