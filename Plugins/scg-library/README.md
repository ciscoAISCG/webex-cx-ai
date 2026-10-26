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
> **Set the Codex task permission to `Ask for Approval`, then copy and paste:**

```text
Install the SCG Library plugin from the AI SCG marketplace in
ciscoAISCG/webex-cx-ai using branch main. Before beginning, confirm this task
can request approval to update the local Codex configuration. If approval is
unavailable, stop and tell me to set the task permission to Ask for Approval.
Do not use sudo or change filesystem permissions. Read the live plugin README
first. Do not ask me to run terminal commands; perform the required Codex
plugin-management steps yourself. If the ai-scg marketplace is not configured,
add it. Preserve all unrelated Codex configuration and ensure the top-level setting
mcp_oauth_callback_port = 5555 is present. Install only scg-library, verify its
source and installed version, and do not access SCG Library business data yet.
Tell me when to fully quit and reopen Codex and give me the exact first-use
prompt.
```

The user may need to approve the scoped edit to Codex configuration. Codex must
preserve every unrelated setting. After installation, fully quit and reopen
Codex, start a new task, and ask:

> Using SCG Library, check my access and list the available data collections.

Codex opens Auth0 for email OTP and consent when authentication is required. The
user enters the email and OTP only in the Auth0 browser—not in Codex. The remote
server automatically records a verified first-time `@cisco.com` user as Active;
other verified domains are Pending until an administrator approves them.
Returning approved users normally continue without another onboarding step,
and administrators can revoke access at any time.

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

Use the canonical [AI SCG marketplace update instructions](../README.md#update-my-plugins).

## Authentication recovery

For any SCG Library login, reconnect, expired-session, or wrong-identity
problem, copy and paste:

```text
Fix my SCG Library authentication. Preserve the installed plugin, AI SCG
marketplace, Codex configuration, Auth0 user, and SCG access registry. Do not
ask me to run terminal commands. Diagnose the authentication state and perform
the least disruptive recovery. Use a normal scg-library MCP reconnect first.
Only if Auth0 repeatedly shows the wrong or stale email identity, I am
switching identities, or a major Auth0 change requires a clean session, log
out of the scg-library MCP and clear only the Auth0 site session for
scg-library.primarydemo.com. Never clear my complete browser history, cache,
or cookies or sign me out of Cisco, Microsoft, or Google; use a private browser
window if a safe site-only reset is unavailable. Start the required login with
the airtable:read and offline_access scopes. Let me enter my email, OTP, and
consent only in the Auth0 browser. After login succeeds, tell me to fully quit
and reopen Codex before checking access. Do not reinstall the plugin or delete
or modify any user or registry record.
```

The user completes email OTP and consent only in the Auth0 browser. The OTP email
is sent after the fresh login begins. Deleting a registry row does not sign the
user out of Auth0; administrators use `Status = Revoked` to block access.

<details>
<summary>Manual authentication fallback</summary>

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
