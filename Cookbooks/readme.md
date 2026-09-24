# AI Agent Cookbook for WxCC

A practical guide for designing, securing, governing, and launching AI agents in WxCC.

## What You'll Find

This cookbook helps teams:
- understand the basics of AI agent design in WxCC
- follow security and governance recommendations
- use consistent templates and patterns
- avoid common mistakes
- move from idea to production in a structured way

## Recommended Reading Order

1. [Getting Started](docs/getting-started.md)
2. [Architecture](docs/architecture.md)
3. [Security](docs/security.md)
4. [Governance](docs/governance.md)
5. [Prompt Design](docs/prompt-design.md)
6. [Agent Template](docs/agent-template.md)
7. [Knowledge and RAG](docs/knowledge-and-rag.md)
8. [Testing and Evaluation](docs/testing-and-evaluation.md)
9. [Deployment and Operations](docs/deployment-and-operations.md)
10. [Human Handoff](docs/human-handoff.md)
11. [Common Pitfalls](docs/common-pitfalls.md)

## Who This Is For

- Engineers building AI agents for WxCC
- Architects defining agent patterns
- Product teams planning AI-powered experiences
- Operations teams supporting deployments
- Anyone new to WxCC AI agent development

## Publishing

This cookbook is structured for GitHub and can also be published as a documentation site using MkDocs and GitHub Pages.

The [Playbooks](docs/playbooks.md) card catalog is generated from the README in each `Playbooks/<playbook-name>/` folder. To refresh it locally after adding or updating a playbook, run:

```powershell
python scripts/generate_playbook_catalog.py
```

The GitHub Pages workflow runs this generator automatically before building the site whenever `Playbooks/`, `Cookbooks/`, or the generator changes.

The [Plugins](docs/plugins.md), [Skills](docs/skills.md), and [MCP Factory](docs/mcp-factory.md) card catalogs are generated from the package folders under `Plugins/`, `Skills Shed/`, and `MCP Factory/servers/`. To refresh all three catalogs locally, run:

```powershell
python scripts/generate_resource_catalogs.py
```

The GitHub Pages workflow refreshes these catalogs automatically whenever one of those source folders or the generator changes.

## Suggested Next Step

Start with [Getting Started](docs/getting-started.md).
