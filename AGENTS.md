# AI SCG contribution instructions

These instructions are the repository contract for Codex and other coding
agents contributing to `ciscoAISCG/webex-cx-ai`.

## Default contribution path

- Package reusable team capabilities as marketplace plugins by default.
- Use `Skills/` only when the user explicitly wants a standalone,
  manually-installed skill.
- Inspect the existing repository before choosing names or paths. Preserve
  existing assets and avoid duplicate capabilities.
- Ask no more than two targeted questions, and only when the answer cannot be
  inferred and would change package identity, scope, authentication, or data
  handling. Otherwise proceed.

## Marketplace plugins

- Create plugins under `Plugins/<plugin-name>/` using a stable, lower-case,
  hyphenated name.
- Every plugin must include `.codex-plugin/plugin.json` with the same `name`, a
  valid semantic `version`, an AI SCG author, and complete interface metadata.
- Put bundled skills under `Plugins/<plugin-name>/skills/<skill-name>/SKILL.md`.
- A plugin may contain one skill, multiple skills, an MCP server, an app, or a
  supported combination.
- For a new plugin, add exactly one matching entry to
  `.agents/plugins/marketplace.json` with a `./Plugins/<plugin-name>` source.
- For an update, preserve the folder, manifest name, and marketplace identity.
  Update the contents and increment the manifest version; never create a
  numbered replacement folder.
- Use the built-in plugin-creation workflow when available, but treat this
  repository contract and its validator as authoritative.

## Standalone skills

- Create standalone skills under `Skills/<skill-name>/SKILL.md`.
- Use a lower-case, hyphenated skill name and include concise `name` and
  trigger-oriented `description` frontmatter.
- Keep only scripts, references, and assets that the workflow needs.
- If the skill is intended for marketplace distribution, package it under
  `Plugins/` instead of duplicating it in both locations.

## Validation and publishing

- Never include credentials, tokens, customer data, or private internal data.
- Run `python3 scripts/validate_contributions.py` before committing.
- Run relevant skill or plugin tests in addition to the repository validator.
- Use a feature branch named `users/<github-login>/<short-task>` and open a
  pull request to `main`.
- In the pull request, summarize the capability, changed paths, validation, and
  risks or follow-up.
- Do not merge without human review. Delete the feature branch only after the
  pull request is confirmed merged.
