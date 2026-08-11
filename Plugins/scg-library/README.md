# SCG Library Codex Plugin

Secure, read-only access to the SCG Library from Codex. The current business
data is stored in Airtable, but users interact with it as the SCG Library.

## What is packaged

- Remote MCP endpoint: `https://www.primarydemo.com/airtable_access_v1/mcp`
- Public Auth0 native-client identifier
- Cisco-domain auto-approval, external-domain administrator approval, and revocation
- Table discovery, full schema inspection, all-field search, and single-record retrieval guidance

No Airtable PAT, Auth0 client secret, Render secret, or MCP bearer token is included.

## Installation

> [!IMPORTANT]
> **Copy and paste the prompt below into Codex.**
>
> Codex performs the marketplace, configuration, and plugin installation.
> Authentication begins only after the restart and first SCG Library request.

```text
Install the SCG Library plugin from the AI SCG marketplace in
ciscoAISCG/webex-cx-ai using branch main. Read the live plugin README first. Do
not ask me to run terminal commands; perform the required Codex plugin-management
steps yourself. If the ai-scg marketplace is not configured, add it. Preserve
all unrelated Codex configuration and ensure the top-level setting
mcp_oauth_callback_port = 5555 is present. Install only scg-library, verify its
source and installed version, and do not start MCP authentication or access SCG
Library business data during installation. Tell me when to fully quit and reopen
Codex and give me the exact first-use prompt.
```

The user may need to approve the scoped edit to Codex configuration. Codex must
preserve every unrelated setting. After installation, fully quit and reopen
Codex, start a new task, and ask:

> Using SCG Library, check my access and list the available data collections.

The first request starts one app-managed Auth0 transaction in Codex. While that
secure browser flow is open, Codex must not also run `codex mcp login` or open a
second OAuth transaction. The user enters the email and OTP only in the Auth0
browser—not in the conversation. The remote server automatically records a
verified first-time `@cisco.com` user as Active; other verified domains are
Pending until an administrator approves them. Returning approved users normally
continue without another onboarding step, and administrators can revoke access
at any time.

<details>
<summary>Manual installation fallback</summary>

Use these commands only when Codex cannot perform the installation directly:

```bash
codex plugin marketplace add https://github.com/ciscoAISCG/webex-cx-ai.git
codex plugin add scg-library@ai-scg
```

Before authentication, ensure this top-level setting exists in
`~/.codex/config.toml`:

```toml
mcp_oauth_callback_port = 5555
```

</details>

## Updates

Use the canonical [AI SCG marketplace update instructions](../README.md#consumers-check-for-updates).

## Authentication recovery

If Codex reports `Not logged in`, `Auth required`, or an expired Auth0 session,
paste this request instead of reinstalling the plugin or changing the access
registry:

```text
Reconnect SCG Library authentication without reinstalling anything. Start by
checking my SCG Library access once so Codex can open its app-managed Auth0
browser. If that browser opens, wait for me to finish it and do not also run
codex mcp login. Use the command-line MCP login with airtable:read and
offline_access only if no app-managed authentication window opened or that
single flow failed. Before using the fallback, confirm no other SCG Library
OAuth transaction remains open. Preserve my plugin and unrelated configuration,
and tell me whether a full Codex restart is required.
```

The user completes email OTP and consent only in the Auth0 browser. The OTP email
is sent after the fresh login begins. Deleting a registry row does not sign the
user out of Auth0; administrators use `Status = Revoked` to block access.

<details>
<summary>System-browser authentication fallback</summary>

Use this only when the app-managed Auth0 window did not open or failed. It opens
the computer's default browser. Never run it while an embedded Codex Auth0 flow
is active.

```bash
codex mcp login scg-library --scopes airtable:read,offline_access
```

</details>

## Read-only tools

- `get_my_airtable_access_v1`
- `list_airtable_tables_v1`
- `describe_airtable_table_v1`
- `search_airtable_records_v1`
- `query_airtable_records_v2`
- `aggregate_airtable_records_v2`
- `get_airtable_record_v1`

The MCP access registry is never searchable.
