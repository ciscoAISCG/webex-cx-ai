# Skills

Personal-assistant skills for repeatable Webex CX AI workflows.

> **Marketplace or standalone?** Put a standalone, manually installed skill in
> `Skills/`. To distribute a skill through the AI SCG Plugin Marketplace,
> package it as a plugin by following the [Plugins contributor guide](../Plugins/README.md#contributors-ask-codex).

## Contributors: ask Codex

Give Codex your files or describe the workflow, then say:

> Create or update this as a standalone AI SCG skill in the `Skills/` folder of
> `ciscoAISCG/webex-cx-ai`. Follow the existing repository conventions, validate
> the skill, scan it for secrets and customer data, and prepare a feature-branch
> pull request. Do not merge it.

Codex should handle the folder structure, `SKILL.md`, supporting files,
validation, and GitHub workflow. The contributor only needs to review and merge
the pull request.

The minimum published structure is:

```text
Skills/<skill-name>/
└── SKILL.md
```

## Skills

| Skill | Purpose |
| --- | --- |
| [WhatsApp SIP Gateway](./whatsapp/) | Build, deploy, and troubleshoot a Meta WhatsApp Calling SIP gateway for Cisco Webex Contact Center and Webex AI Agents. |
| [AI Calculator](./AI%20Calculator/) | Skill workspace for ROI CC Calculations. |
| [Webex MCP Onboarding](./webex-mcp-onboarding/) | Guided assistant skill for onboarding MCP servers into Webex Developer Portal, Control Hub Agentic Apps, and AI Agent Studio. |
| [AWS SigV4 MCP Onboarding](./aws-sigv4-mcp-onboarding/) | Securely validate and connect AWS IAM SigV4-protected AgentCore MCP servers to Codex and other STDIO-capable MCP clients. |
| [AI Agent Creator](./webex-ai-agent-creator/) | A skill for helping create an AI Agent using all of the best practices. |
