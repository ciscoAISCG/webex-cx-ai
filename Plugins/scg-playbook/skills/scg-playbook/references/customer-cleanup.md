# Customer Cleanup

Before a playbook is customer-facing, remove or replace sensitive and personal material.

## Remove Or Replace

- Full real names, email addresses, and personal phone numbers.
- Customer names, tenant names, org IDs, tenant IDs, queue IDs, queue names, and location IDs unless explicitly approved.
- API keys, bearer tokens, MCP custom header values, passwords, secrets, and webhook signing keys.
- Production URLs that expose private infrastructure.
- Real account, payment, patient, government ID, or support case data.

## Safer Defaults

- Use first names only in examples, such as `Niko` or `Avery`.
- Use fake phone numbers and demo-safe email domains.
- Refer to tenant-specific items as "your queue", "your AI agent", or "your MCP server".
- Explain that importers must rebind IDs, queues, endpoints, and credentials after import.

## Export Sanitization

Preserve raw exports when importability matters. If the user asks to sanitize a JSON export, warn that changing embedded IDs, variables, URLs, or flow references may break import or require manual rebinding.

For internal-only drafts, sensitive values can remain in local artifacts only if they are needed for import testing and the user approves. Do not expose them in README prose.
