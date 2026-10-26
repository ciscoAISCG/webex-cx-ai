# Webex CX AI GitHub Reader

Ask questions about the current contents of the
[`ciscoAISCG/webex-cx-ai`](https://github.com/ciscoAISCG/webex-cx-ai) repository.
The plugin covers the full repository, with focused guidance for Cookbooks,
individual cookbooks, Skills, AI SCG Plugins, and Playbooks.

## How it accesses GitHub

The repository is public. When internet-enabled tools are available, the skill
reads current GitHub content directly and does not require a GitHub token or
connector installation. For issues, pull requests, private repositories, or
environments without a web-capable tool, Codex can guide the user to connect a
GitHub integration. The plugin never asks users to paste a token into chat.

## Optional GitHub token setup

Only create a token if the user requests token-based access or their chosen
GitHub MCP integration requires one. Public repository reading does not need a
token. Use a fine-grained personal access token with access limited to this
repository and read-only permissions:

1. On GitHub, open **Settings → Developer settings → Fine-grained personal
   access tokens → Generate new token**.
2. Select `ciscoAISCG` as the resource owner and **Only select repositories**,
   then choose `webex-cx-ai`.
3. Set **Contents: Read-only**. Add **Issues: Read-only** and **Pull requests:
   Read-only** only if the user also needs GitHub discussions and PR data.
   Repository metadata is read-only by default. Do not grant write permissions.
4. Set an expiration, generate the token, and store it in a secure credential
   store or in the user's environment variable `GITHUB_PAT_TOKEN`. For an
   organization-owned repository, the organization may require approval.
5. Connect the GitHub hosted read-only MCP server to Codex using the saved
   environment variable (never the token text):

   ```bash
   codex mcp add github --url https://api.githubcopilot.com/mcp/x/all/readonly --bearer-token-env-var GITHUB_PAT_TOKEN
   ```

   If `github` is already configured, update that server's URL and credential
   through Codex's MCP configuration instead of adding a duplicate. Fully
   restart Codex after changing the environment variable, then ask it to use
   the GitHub MCP connection for the repository query.

Never paste the token into Codex chat, a terminal command, this repository, a
plugin manifest, or a committed `.env` file. If the token is exposed, revoke it
in **GitHub Settings → Developer settings → Fine-grained personal access
tokens** and create a replacement.

## Installation

> [!IMPORTANT]
> Set the Codex task permission to `Ask for Approval`, then copy and paste:

```text
Install the Webex CX AI GitHub Reader plugin from the AI SCG marketplace in
ciscoAISCG/webex-cx-ai using branch main. Before beginning, confirm this task
can request approval to update the local Codex configuration. If protected-write
approval is unavailable, stop and tell me to set the task permission to Ask for
Approval. Do not use sudo, change filesystem permissions, or attempt another
workaround. Read the plugin README first. Do not ask me to run terminal commands;
perform the marketplace and plugin setup yourself. If the ai-scg marketplace is
not configured, add it. Install only webex-cx-ai-github-reader, preserve
unrelated configuration, and verify the installed source and version. Do not
request a GitHub token for public repository reading. If this environment has no
internet-enabled GitHub access, guide me through connecting an approved GitHub
integration without asking me to paste credentials into chat.
```

## Updates

Use the canonical [AI SCG marketplace update instructions](../README.md#update-my-plugins).

## Example questions

- Find Cookbooks or individual cookbook guidance for a topic and summarize the
  relevant files.
- Explain a Skill or find the right Skill for a task.
- Find an AI SCG plugin, explain its capabilities, or summarize its install
  instructions.
- Find and compare Playbooks relevant to a use case.
- Search the wider repository for current guidance and provide source links.
