# MCP Factory

MCP Factory is the repository home for MCP server configuration files, examples, and setup assets used by the AI SCG team.

Airtable is currently the source of truth for the live MCP server catalog, including descriptions, prerequisites, quick starts, prompts, setup videos, demo videos, and ownership details.

## Server Index

| Server | Airtable Record | Repository Folder | Status |
| --- | --- | --- | --- |
| Mem0 | [View in Airtable](https://airtable.com/appUJj24OxwiVXkGr/pagDx8tr66SCJbgPa/rec0tFReN8TeoIyem?home=pagB18fxYi4MDBi4f) | [servers/mem0](./servers/mem0/) | Cataloged |
| Salesforce | [View in Airtable](https://airtable.com/appUJj24OxwiVXkGr/pagDx8tr66SCJbgPa/recvZjvYRp2DPUqD4?home=pagB18fxYi4MDBi4f) | [servers/salesforce](./servers/salesforce/) | Cataloged |

## Repository Structure

```text
MCP Factory/
  readme.md
  registry.yml
  servers/
    <server-slug>/
      README.md
      config.example.json        # optional/future public example
```

Each server folder is the durable GitHub destination for that MCP server. Keep the detailed catalog content in Airtable and use this repo for versioned technical assets such as config examples, templates, schemas, implementation notes, and reusable setup files.

## Contribution Notes

- Add one folder per MCP server under `servers/`.
- Use lowercase URL-friendly slugs for folder names, such as `mem0`.
- Link each server folder back to its Airtable record.
- Do not commit secrets, API keys, OAuth tokens, private endpoints, customer data, or tenant-specific credentials.
- Use placeholders in example config files when real values are required.
