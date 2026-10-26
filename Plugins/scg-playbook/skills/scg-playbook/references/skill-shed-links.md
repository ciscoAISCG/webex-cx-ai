# Skills Links

Skills is a shared GitHub repo destination, not a local folder in the `one_drive` skill-source project.

## Local Structure Rule

- Source skill folders live at `one_drive/<skill-name>/`.
- Installed test copies live at `/Users/ntheolog/.codex/skills/<skill-name>/`.
- Do not create `one_drive/Skills/` unless the user explicitly says the current checkout is the target GitHub repo.

## Playbook Link Pattern

When a playbook should point readers to a helper skill in the future shared repo, use a relative link placeholder:

```html
<a href="../../Skills/webex-mcp-onboarding/" style="display:inline-block;background:#1f6feb;color:#ffffff;padding:10px 18px;border-radius:999px;text-decoration:none;font-weight:700;">Open Skills: Webex MCP onboarding skill</a>
```

Use the skill name plainly in prose:

```markdown
Use `webex-mcp-onboarding` when you are new to MCP onboarding in Control Hub and AI Agent Studio.
```

If GitHub strips inline styles, use this fallback:

```markdown
> [!NOTE]
> **Skills helper:** [Open Webex MCP onboarding skill](../../Skills/webex-mcp-onboarding/)
```
