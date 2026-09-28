# Call Summary Transfer Lambda

This TypeScript AWS SAM project receives the Webex Contact Center
`task:consulting` webhook, retrieves the interaction's `MID_CALL` summary,
resolves the consulted Webex Calling user, and sends that user a direct Webex
message.

For the complete architecture, OAuth scopes, webhook configuration, validation,
and security guidance, see the published
[FDE playbook](https://webexcc-sa.github.io/FDE-Playbook-Catalog/playbooks/consult-transfer-summary-to-webex/).

## Configure

Use `.env.example` as the environment-variable reference. Do not put a real
token or client secret in the source tree.

The demo defaults to:

- `EXTENSION_LENGTH=4`, so a short internal dial string such as `011005`
  resolves to extension `1005`;
- preserving formatted or 10-or-more-digit PSTN numbers as received;
- `DRY_RUN=true` until the resolved destination and Webex person are verified;
- logging the webhook body for controlled POC troubleshooting only.

## Test and build

```bash
npm ci
npm run quality
sam validate --lint
sam build
```

## Deploy

```bash
sam deploy --guided
```

Use the resulting `WebhookUrl` as the destination of the Webex Contact Center
subscription for `task:consulting`. Keep `DRY_RUN=true` for the first test, then
follow the validation checklist in the published playbook before enabling real
message delivery.

The included Lambda Function URL uses unauthenticated ingress for this POC. Add
webhook verification, asynchronous processing, retries, idempotency, managed
secrets, and production-safe logging before using the design in production.
