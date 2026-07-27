---
name: aws-sigv4-mcp-onboarding
description: Securely connect, validate, and troubleshoot AWS IAM SigV4-protected Streamable HTTP MCP servers from Codex or another STDIO-capable MCP client. Use when a user provides an Amazon Bedrock AgentCore Runtime or Gateway MCP endpoint, runtime ARN, AWS region, profile, access-key-based credentials, IAM role, or SSO profile and asks to add, configure, test, reproduce, or diagnose that MCP connection. Use the maintained mcp-proxy-for-aws bridge; never collect, print, or commit AWS secret values.
---

# AWS SigV4 MCP Onboarding

Connect an IAM-protected remote MCP through AWS's local SigV4 bridge. Keep the remote server on Streamable HTTP; expose the bridge to the client as a local STDIO MCP server.

## Required Inputs

Collect:

- A safe local MCP server name chosen by the operator. This is only the label
  shown inside Codex or another client, not an AWS value supplied by the
  customer. Prefer a descriptive name such as `customer-webex`.
- The complete HTTPS AgentCore invocation or gateway MCP endpoint.
- The runtime ARN when AgentCore Runtime is used.
- The AWS region.
- A local AWS profile name chosen by the operator, such as `customer-mcp`.
- Whether to restrict discovery to tools marked read-only.

Never ask the user to paste an access key, secret key, session token, password, or SSO code into chat. Never write credentials into the skill, plugin, generated client configuration, command arguments, or logs.

## Workflow

### 1. Confirm SigV4 is the correct path

Use this workflow only when the remote MCP requires AWS IAM SigV4. If the server uses OAuth/JWT or a bearer token, configure it as a direct Streamable HTTP MCP instead.

Use `mcp-proxy-for-aws` as the bridge. Do not build a second remote MCP server or implement custom request signing.

### 2. Validate public connection identifiers first

Run the offline check before touching credentials or Codex configuration:

```bash
python3 scripts/sigv4_mcp.py check \
  --server-name "<local-name>" \
  --endpoint "<https-endpoint>" \
  --runtime-arn "<runtime-arn>" \
  --region "<region>" \
  --profile "<profile>" \
  --offline
```

Stop if the ARN encoded in the URL does not exactly match the supplied runtime ARN, or if the endpoint host, ARN, and requested region disagree. Do not guess which identifier is authoritative.

The check reports whether the account, region, partition, or runtime ID differs.
Ask the AWS owner which complete runtime ARN is authoritative. After the owner
confirms it, derive the corresponding endpoint deterministically:

```bash
python3 scripts/sigv4_mcp.py endpoint-from-arn \
  --runtime-arn "<confirmed-runtime-arn>" \
  --confirm-authoritative
```

Do not use this command merely because two identifiers differ. The explicit
confirmation flag records that the owner has resolved the ambiguity.

### 3. Establish credentials outside Codex

Prefer, in order:

1. AWS IAM Identity Center/SSO profile.
2. An assumed-role profile with short-lived credentials.
3. A narrowly scoped static access-key profile only when the customer requires it.

Have the user configure or authenticate the profile in their own terminal. For static credentials, direct them to:

```bash
aws configure --profile "<profile>"
```

Do not run a command containing a secret as an argument. If a secret was pasted into chat, a ticket, a document, or source control, recommend rotation before continuing.

### 4. Verify the resolved AWS identity

Run:

```bash
python3 scripts/sigv4_mcp.py check \
  --server-name "<local-name>" \
  --endpoint "<https-endpoint>" \
  --runtime-arn "<runtime-arn>" \
  --region "<region>" \
  --profile "<profile>"
```

Report only the resolved principal ARN and account. A caller may be in a different AWS account when cross-account resource policies permit it; do not require the caller account to equal the runtime account.

### 5. Render and review the client configuration

For Codex:

```bash
python3 scripts/sigv4_mcp.py render \
  --client codex \
  --server-name "<local-name>" \
  --endpoint "<https-endpoint>" \
  --runtime-arn "<runtime-arn>" \
  --region "<region>" \
  --profile "<profile>"
```

For a JSON-configured MCP client:

```bash
python3 scripts/sigv4_mcp.py render \
  --client json \
  --server-name "<local-name>" \
  --endpoint "<https-endpoint>" \
  --runtime-arn "<runtime-arn>" \
  --region "<region>" \
  --profile "<profile>"
```

Add `--read-only` only when the user wants tools not annotated `readOnlyHint=true` hidden.

### 6. Register with Codex

When the user has asked to connect or install the server, run:

```bash
python3 scripts/sigv4_mcp.py install-codex \
  --server-name "<local-name>" \
  --endpoint "<https-endpoint>" \
  --runtime-arn "<runtime-arn>" \
  --region "<region>" \
  --profile "<profile>"
```

The installer refuses to replace an existing MCP registration. Inspect the existing registration and obtain explicit approval before removing or replacing it.

### 7. Validate end to end

Require all of:

1. `codex mcp list` shows the expected enabled server.
2. Codex is fully restarted and a new task is opened.
3. MCP initialization and `tools/list` succeed.
4. A harmless read-only tool call succeeds when an appropriate tool exists.

Do not treat successful profile validation as proof that the runtime IAM policy permits invocation.

## References

- Read `references/client-patterns.md` when configuring clients other than Codex or explaining the bridge.
- Read `references/security-and-iam.md` for credential handling and least-privilege IAM.
- Read `references/troubleshooting.md` for authentication, endpoint, region, session, or startup failures.

## Boundaries

- Keep customer secrets out of every artifact and response.
- Pin the proxy version for reproducibility; update it deliberately after validation.
- Do not modify an existing AWS profile.
- Do not remove or replace an existing MCP registration without explicit approval.
- Do not claim that `--read-only` is an authorization boundary. IAM and server-side policy remain authoritative.
