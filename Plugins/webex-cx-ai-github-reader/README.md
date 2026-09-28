# Webex CX AI GitHub Reader Codex Plugin

Read and query files, issues, and pull requests in
[`ciscoAISCG/webex-cx-ai`](https://github.com/ciscoAISCG/webex-cx-ai) through
GitHub's hosted read-only MCP server.

## What it connects

- MCP endpoint: `https://api.githubcopilot.com/mcp/readonly`
- Authentication: each installer supplies their own fine-grained GitHub token
  through the local `GITHUB_PAT_TOKEN` environment variable.
- Permissions: read-only repository contents, issues, and pull requests.

The `/readonly` endpoint exposes only read tools. The repository config stores
only the environment-variable name; it contains no token. The skill directs
queries to `ciscoAISCG/webex-cx-ai`.

## Installation

> [!IMPORTANT]
> Set the Codex task permission to `Ask for Approval`, then copy and paste:

```text
Install the Webex CX AI GitHub Reader plugin from the AI SCG marketplace in
ciscoAISCG/webex-cx-ai using branch main. Before beginning, confirm this task
can request approval to update the local Codex configuration. If protected-write
approval is unavailable, stop and tell me to set the task permission to Ask for
Approval. Do not use sudo, change filesystem permissions, or attempt another
workaround. Read this plugin README first. Install only
webex-cx-ai-github-reader, preserve unrelated configuration, and verify the
installed source and version. Check whether GITHUB_PAT_TOKEN is available
without displaying its value. If it is missing, guide me through creating a
fine-grained token and saving it as a local user environment variable; never
ask me to paste the token into Codex or commit it. Do not query GitHub until the
token is configured. After setup, tell me to fully restart Codex so it can read
the environment variable.
```

To create the token, open GitHub **Settings → Developer settings → Fine-grained
personal access tokens → Generate new token**:

1. Choose `ciscoAISCG` as the resource owner.
2. Under repository access, choose **Only select repositories** and select
   `webex-cx-ai`.
3. Grant **Contents: Read-only**, **Issues: Read-only**, and **Pull requests:
   Read-only**. Metadata is required and is read-only by default.
4. Save the token in your operating system's user environment variables under
   the name `GITHUB_PAT_TOKEN`. Do not put it in this repository, a plugin
   manifest, or a committed `.env` file.
5. Fully quit and reopen Codex after setting the variable.

An organization may require an administrator to approve the fine-grained token.
GitHub fine-grained tokens also have read-only access to public repositories;
the plugin skill scopes its queries to the named AI SCG repository, but this
hosted MCP endpoint does not enforce a single-repository boundary. For private
repositories, selecting only `webex-cx-ai` limits the token's private-repo
access to that repository.

## Use with other MCP clients

The GitHub endpoint is a standard remote MCP server. In another MCP-capable AI
tool, configure the URL above and provide the same bearer token through that
tool's secure credential or environment-variable mechanism. Client setup and
secret-store syntax vary; never paste a token into a shared plugin file or
commit it.

## Updates

Use the canonical [AI SCG marketplace update instructions](../README.md#update-my-plugins).
