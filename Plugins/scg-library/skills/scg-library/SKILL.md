---
name: scg-library
description: Securely query the SCG Library from Codex. Use when a user asks an SCG business-data question, checks their SCG Library access, lists or describes available data collections, searches across the wide underlying Airtable dataset, finds matching customer or opportunity records, requests counts or summaries, or retrieves one complete record. The bundled remote MCP is read-only, authenticates through Auth0 email, auto-approves verified Cisco identities, requires administrator approval for other domains, and honors revocation.
---

# SCG Library

Use the bundled `scg-library` remote MCP server. Never ask the user for an Airtable personal access token, Auth0 secret, Render secret, or permanent MCP token.

## Mandatory tool discovery

Plugin MCP tools may be deferred instead of appearing in the task's initial tool list. Before concluding that the connector or access-check tool is unavailable:

1. Search the available and deferred tools once for the exact tool name `get_my_airtable_access_v1` and the server/plugin name `scg-library`.
2. Load or invoke the discovered `mcp__scg_library__get_my_airtable_access_v1` tool.
3. Do not tell the user to start another Codex task merely because the tool was not initially visible.

Only report a connector-loading failure after this focused discovery attempt returns no matching tool or the discovered tool produces an actual startup error. Preserve and report the safe startup error instead of claiming that the user's configuration is correct without evidence.

Treat all of these results as the same recoverable authentication state:

- `Auth required`
- `Not logged in`
- `authentication_required`
- an expired or timed-out OAuth/Auth0 session
- no usable stored OAuth credentials

Do not stop after reporting one of these messages, claim a specific token
lifetime caused it without evidence, or direct the user to Codex Settings or
Connectors. This plugin's remote MCP authentication is managed by the Codex
CLI. Explain that no SCG Library business data was accessed, then run this
exact recovery command directly when terminal execution is available. If it is
not available, give the user the command without asking them for credentials:

```bash
codex mcp login scg-library --scopes airtable:read,offline_access
```

Wait for the browser email OTP and consent flow to complete successfully. The
OTP email is triggered by this fresh login flow, not by deleting an Airtable
registry row. Then the user must fully quit Codex with `Cmd-Q` on macOS or Exit
on Windows, reopen it, start a new task, and retry. Closing only the window or
starting another task without restarting the app does not reload the MCP
session. Do not report the recovery as complete until the login command exits
successfully.

## First-use check

Before the first MCP call in a task, verify that Codex uses the registered Auth0 callback port:

```toml
mcp_oauth_callback_port = 5555
```

This is a top-level setting in `~/.codex/config.toml`. If it is already present with value `5555`, continue. If it is absent or different, explain that Auth0 requires the registered callback and help the user add or correct this one setting before authenticating. Do not overwrite unrelated Codex configuration.

## Access flow

Before opening Auth0 for initial authentication or reauthentication, explain
the following in plain language:

> SCG Library uses Auth0 to verify your business email with a one-time code.
> Your verified email becomes your identity in the SCG Library access
> registry. This plugin never asks for or sees your email password. Airtable
> access is read-only. Verified `@cisco.com` identities are approved
> automatically; other business domains require administrator approval. An
> administrator can revoke access at any time. A secure browser page will open
> next; close it and stop if the page is unexpected.

Do not ask the user to share their email address or OTP in Codex. The user must
enter both directly in the Auth0 browser flow.

For a user's first SCG Library request in a task:

1. Call `get_my_airtable_access_v1`.
2. If Auth0 prompts, let the user complete email OTP and consent in the browser.
3. A verified first-time `@cisco.com` user is registered as `Active`. Every
   other verified domain is registered as `Pending` for administrator approval.
4. Continue when the tool returns `status: active`.

If the result is `access_pending`:

- Explain plainly that the email was verified and the access request was
  recorded, but an administrator must approve it.
- Do not call a business-data tool while access is Pending.
- Do not rerun Auth0 or ask the user to reinstall; approval is completed by an
  administrator changing the registry Status from `Pending` to `Active`.

If the result is `access_revoked`:

- Explain plainly that the administrator has revoked this identity's access.
- Do not attempt any business-data tool.
- Do not suggest reinstalling, requesting a new form, or bypassing the registry.

If the result is `access_denied`, `authentication_required`, or `authorization_required`, report the exact safe message returned by the tool. Guide the user through Auth0 again only for an authentication or authorization result. Never request or expose raw OAuth tokens.

There is no separate access-request form. Auth0 verification automatically
creates the registry entry: allowed domains become Active and other domains
become Pending. The server enforces Active, Pending, or Revoked status on every
business-data call.

## Natural-language query workflow

The user is not expected to know table names, field names, record IDs, query
operators, or MCP tool names. Never pass the user's entire natural-language
question as one literal search string. First classify and decompose it.

1. Identify the intent:
   - literal entity lookup
   - filtered record list
   - exact count or group-by summary
   - complete record
   - cross-table or related-record question
2. Extract literal entities, such as a customer or opportunity name, separately
   from constraints such as status, date range, missing value, flag, or asset.
3. Use `list_airtable_tables_v1` only when table discovery is needed.
4. Use `describe_airtable_table_v1` to map business language to actual fields
   before a structured query. Reuse the schema already returned in the task.
5. Choose the smallest useful query:
   - Use `query_airtable_records_v2` with `engine: "auto"` for lookups and
     filtered lists. Select relevant tables, search fields, return fields, and
     structured filters instead of searching everything by default.
   - Use `aggregate_airtable_records_v2` for exact counts and group-by questions.
   - Use several focused V2 calls for cross-table questions, following linked
     record IDs or shared customer names only when supported by returned data.
   - Use `get_airtable_record_v1` when one complete record is needed and its
     table plus record ID are known.
   - Use `search_airtable_records_v1` only for an explicit V1 baseline,
     troubleshooting, or when the user asks to compare engines.

V2 filters are objects with `field`, `operator`, and usually `value`. Supported
operators are `eq`, `neq`, `contains`, `not_contains`, `gt`, `gte`, `lt`, `lte`,
`is_empty`, `is_not_empty`, and `in`. Use `filter_logic: "and"` or `"or"`.
Structured filtering and sorting require exactly one table, so decompose
cross-table questions into separate calls.

When the user asks for a V1/V2 comparison, run the same literal lookup through
`query_airtable_records_v2` twice with `engine: "v1"` and `engine: "v2"`.
Keep table, search fields, and limit identical. Compare correctness first, then
the returned benchmark metrics: requests, elapsed time, rate-limit retries,
tables, fields, chunks, and records. Do not run both engines on every normal
question because that doubles Airtable traffic.

Summarize matches clearly with collection or table name, record ID, and the fields that answer the question. If no records match, say so and offer a concise alternative search phrase. Never invent records or answer from general knowledge when the user asked about the SCG Library.

## Security boundaries

- Business data is read-only. There is no business-table create, update, or delete operation.
- Never suggest bypassing Auth0, revocation, or the `airtable:read` scope.
- Never search for or expose the access-registry table.
- Treat returned records as user-requested business data; include only what is relevant to the question.
- Do not expose internal credentials, OAuth tokens, authorization headers, or server environment variables.

## Available tools

- `get_my_airtable_access_v1`
- `list_airtable_tables_v1`
- `describe_airtable_table_v1`
- `search_airtable_records_v1`
- `query_airtable_records_v2`
- `aggregate_airtable_records_v2`
- `get_airtable_record_v1`
