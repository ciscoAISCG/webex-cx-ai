---
name: scg-update-lab
description: Test which release of the isolated SCG Plugin Update Lab is currently loaded in Codex. Use only when a user explicitly asks about the SCG update lab, plugin update prototype, installed lab release, or update verification. Never use this test skill for SCG Library, Airtable, customer, implementation, opportunity, or production questions.
---

# SCG Plugin Update Lab

Treat this as a non-production test plugin. Never access SCG Library, Airtable,
Auth0, customer information, implementation information, or any production MCP
server.

## Report the installed release

Return these two values exactly:

```text
LAB_RELEASE=v1
LAB_MESSAGE=Initial marketplace installation is active.
```

State that the values belong to the isolated SCG Plugin Update Lab, not a
working or production SCG plugin.

When asked to verify an update, report the installed release exactly as written
above. Do not infer or claim that a newer release exists.
