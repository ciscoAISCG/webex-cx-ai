# Troubleshooting

## Runtime ARN does not match endpoint

Cause: The supplied runtime ARN and URL-encoded ARN identify different accounts, regions, or runtime IDs.

Action:

1. Stop before configuring credentials or registering the MCP.
2. Report the differing components exactly: AWS account, region, partition,
   and/or runtime ID.
3. Ask the AWS owner which complete runtime ARN is authoritative.
4. After explicit confirmation, derive the endpoint rather than editing the
   encoded URL manually:

   ```bash
   python3 scripts/sigv4_mcp.py endpoint-from-arn \
     --runtime-arn "<confirmed-runtime-arn>" \
     --confirm-authoritative
   ```

5. Re-run the offline `check` with the confirmed ARN and derived endpoint.

Do not infer the authoritative account from the access key. Cross-account
invocation can be valid, so the caller account is not proof of runtime
ownership.

## Customer asks for the MCP server name

The `--server-name` value is not supplied by the customer or AWS. It is a local
label for the connection in Codex or another MCP client. Choose a relevant,
collision-free name such as `customer-webex`. Keep it distinct from:

- The AgentCore runtime ID.
- The runtime ARN.
- The AWS CLI profile name.
- Tool names returned by the remote MCP.

## `403 ACCESS_DENIED`

Possible causes:

- The request was unsigned.
- The profile resolved to the wrong principal.
- The SigV4 service or region is wrong.
- Identity policy lacks `bedrock-agentcore:InvokeAgentRuntime`.
- The runtime resource policy does not allow the caller.
- Temporary credentials expired or omitted the session token.

Run the live `check` command, verify the resolved principal, and have the AWS owner inspect both identity and resource policies.

## `401 Unauthorized`

An AgentCore runtime configured for OAuth/JWT returns an authentication challenge rather than accepting IAM SigV4. Confirm the runtime's inbound authentication mode. Use a direct Streamable HTTP OAuth connection when OAuth is authoritative.

## `NoRegionError` or invalid request parameters

Pass `--region` explicitly and confirm the profile has a region:

```bash
aws configure get region --profile <profile>
```

## `uvx` missing

Install the approved `uv` distribution for the workstation, verify `uvx --version`, and retry. Do not silently fall back to an unpinned package installer.

## Slow first startup

The first `uvx` launch may download and cache the pinned proxy package. Increase the MCP startup timeout if the client times out during this first launch, then retry.

## Server appears installed but tools are unavailable

1. Fully quit and reopen the client.
2. Start a new task/session.
3. Confirm the MCP registration is enabled.
4. Inspect proxy stderr without enabling credential or HTTP-header logging.
5. Re-run `tools/list`.

## Session or cold-start behavior

AgentCore returns `Mcp-Session-Id`. The client/bridge must reuse it for subsequent requests. Upgrade the pinned proxy only after testing if session handling appears defective.
