# SCG Library Codex Plugin

Secure, read-only access to the SCG Library from Codex. The current business
data is stored in Airtable, but users interact with it as the SCG Library.

## What is packaged

- Remote MCP endpoint: `https://www.primarydemo.com/airtable_access_v1/mcp`
- Public Auth0 native-client identifier
- Cisco-domain auto-approval, external-domain administrator approval, and revocation
- Table discovery, full schema inspection, all-field search, and single-record retrieval guidance

No Airtable PAT, Auth0 client secret, Render secret, or MCP bearer token is included.

## User installation

Add the AI SCG marketplace once, then install the plugin from that marketplace:

```bash
codex plugin marketplace add https://github.com/ciscoAISCG/webex-cx-ai.git
codex plugin add scg-library@ai-scg
```

The marketplace is the maintained source for future plugin releases. Before the
first authentication, confirm this top-level Codex setting exists in
`~/.codex/config.toml` without changing unrelated configuration:

```toml
mcp_oauth_callback_port = 5555
```

After installation, fully quit and reopen Codex, start a new task, and ask:

> Using SCG Library, find information about ...

Codex opens Auth0 for email OTP and consent when authentication is required. The
remote server automatically records a verified first-time `@cisco.com` user as
Active and then runs the read-only query. Other verified domains are recorded as
Pending until an administrator changes the row to Active. Returning approved
users normally continue without another onboarding step; rotating refresh
tokens prevent daily reconnects. An administrator can block access by setting
the user's registry Status to Revoked.

## Read-only tools

- `get_my_airtable_access_v1`
- `list_airtable_tables_v1`
- `describe_airtable_table_v1`
- `search_airtable_records_v1`
- `query_airtable_records_v2`
- `aggregate_airtable_records_v2`
- `get_airtable_record_v1`

The MCP access registry is never searchable.
