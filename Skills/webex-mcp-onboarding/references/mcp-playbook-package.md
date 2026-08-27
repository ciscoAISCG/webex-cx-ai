# MCP Playbook Package

Use this reference when packaging an MCP setup as a reusable internal/customer playbook.

## Positioning

Describe the skill-guided build as the source of truth and the playbook as the reusable package created from real evidence.

Manager-safe framing:

> Skills make playbook creation more repeatable and easier to validate. The playbook remains the shareable deliverable, but it is produced from a guided, tested build instead of hand-written static steps.

## Playbook Sections

1. Title and target audience.
2. What the MCP-enabled agent does.
3. Platforms used: Webex Developer Portal, Control Hub, AI Agent Studio, and any Flow Designer or Webex Connect dependency.
4. MCP fit assessment, including hosted server ownership, security approval path, and why Webex Connect was not chosen for fulfillment.
5. Official documentation links used.
6. Prerequisites and roles.
7. Developer Portal Agentic App registration.
8. Control Hub provisioning and governance.
9. MCP server/tool inventory.
10. Studio prompt/tool contract.
11. Validation tests and evidence.
12. Troubleshooting.
13. Security and production-readiness notes.
14. Known limitations and tenant-specific assumptions.

## Customer/Partner Cleanup

Remove or generalize:

- Cisco-internal org names.
- Internal-only URLs.
- Private team process.
- Credentials, tokens, tenant IDs, and screenshots with customer data.
- Feature flags or unreleased behavior unless approved.

## Evidence To Attach Or Reference

- Screenshots with sensitive data redacted.
- Exported agent or prompt snippets when allowed.
- Sample test transcript.
- Tool list and enabled status.
- Known-good test payload and response shape.
