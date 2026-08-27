# Client Patterns

## Connection model

The remote server remains a Streamable HTTP MCP. The local bridge signs each upstream request with AWS SigV4 and exposes a standard STDIO MCP interface:

```text
MCP client -> local STDIO -> mcp-proxy-for-aws -> signed Streamable HTTP -> AWS MCP
```

Use AWS's maintained `mcp-proxy-for-aws` package. Pin the validated version instead of using `latest`.

## Codex

`<server-name>` is a local registration label chosen by the Codex operator. It
does not come from AWS or the customer. Use a short descriptive name such as
`customer-webex`; it only identifies the connection inside the MCP client.

Codex registration has this shape:

```bash
codex mcp add <server-name> -- \
  uvx mcp-proxy-for-aws@<version> \
  <endpoint> \
  --service bedrock-agentcore \
  --profile <profile> \
  --region <region>
```

Use `scripts/sigv4_mcp.py render --client codex ...` to quote values safely. Use `install-codex` to validate the AWS identity, refuse collisions, add the server, and confirm its registration.

## JSON-configured MCP clients

Most STDIO-capable clients accept:

```json
{
  "mcpServers": {
    "customer-name": {
      "command": "uvx",
      "args": [
        "mcp-proxy-for-aws@1.6.0",
        "https://example",
        "--service",
        "bedrock-agentcore",
        "--profile",
        "customer-name",
        "--region",
        "us-east-2"
      ]
    }
  }
}
```

Generate this with `scripts/sigv4_mcp.py render --client json ...`. Confirm the target client's current configuration location and restart behavior from that client's documentation.

## Read-only filter

The proxy's `--read-only` option hides tools not annotated with `readOnlyHint=true`. Treat this only as a client-side discovery filter. It does not replace:

- IAM permissions.
- AgentCore resource policies.
- Authorization inside the MCP server.
- Client approval settings.

Start with `--read-only` for unfamiliar customer MCPs when useful tools are correctly annotated. Remove it only when the user is authorized to invoke write-capable tools.
