# SCG Plugin Update Lab

This non-production plugin proves the AI SCG marketplace installation and
update workflow without modifying any working SCG skill, plugin, MCP server, or
configuration.

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
