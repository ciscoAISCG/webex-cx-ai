# Security and IAM

## Credential sources

Prefer:

1. AWS IAM Identity Center/SSO.
2. An assumed role with temporary credentials.
3. A narrow static IAM access key only when required.

The proxy uses the standard AWS credential chain. Store credentials in the AWS CLI profile or approved enterprise credential provider, never in Codex configuration or plugin files.

Static credentials can be entered interactively with:

```bash
aws configure --profile <profile>
```

Temporary credentials also require a session token. Do not assume an access key and secret alone are sufficient.

## Minimum runtime permission

The invoking principal normally needs:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": "<exact-runtime-arn>"
    }
  ]
}
```

Some user-context invocation designs additionally require `bedrock-agentcore:InvokeAgentRuntimeForUser`. Use only the actions required by the customer's runtime design.

The runtime may also require a resource-based policy allowing the caller. Cross-account invocation is valid when identity and resource policies allow it; the caller account does not have to equal the runtime account.

## Secret-handling rules

- Never request secrets in chat.
- Never pass secrets as command-line arguments.
- Never put secrets in `SKILL.md`, plugin manifests, examples, generated JSON, logs, screenshots, tickets, or source control.
- Never echo environment variables that may contain AWS credentials.
- If a long-lived credential was exposed, stop using it and recommend rotation.
- Report only the resolved caller account and principal ARN from `sts get-caller-identity`.

## Authorization boundary

SigV4 authenticates the AWS principal and protects request integrity. IAM and the MCP server decide authorization. HTTPS provides transport encryption. Client-side tool approval and `--read-only` filtering are defense-in-depth controls, not business authorization.
