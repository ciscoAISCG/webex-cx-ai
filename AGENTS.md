# AI SCG Codex instructions

This file routes Codex and other coding agents to the correct AI SCG
contribution standard.

## Current scope

- Specialized zero-training instructions currently exist only for `Plugins/`
  and `Skills/`.
- Do not create specialized instruction files for other top-level folders until
  the AI SCG team agrees on their contribution standards.

## Route the contribution

- Default reusable team capabilities to marketplace distribution. Before
  changing `Plugins/` or `.agents/plugins/marketplace.json`, read and follow
  `Plugins/AGENTS.md`.
- Use `Skills/` only when the user explicitly requests a standalone,
  manually-installed skill. Before changing `Skills/`, read and follow
  `Skills/AGENTS.md`.
- If a request touches both areas, read both scoped instruction files.
- For other asset families, inspect their existing README and structure; do not
  infer that the plugin or skill standards apply.

## Interaction

- Inspect the repository before choosing names or paths. Preserve existing
  assets and avoid duplicate capabilities.
- Ask no more than two targeted questions, and only when the answer cannot be
  inferred and would change package identity, scope, authentication, or data
  handling. Otherwise proceed.

## Shared safety and publishing

- Never include credentials, tokens, customer data, or private internal data.
- Run `python3 scripts/validate_contributions.py` before committing.
- Run relevant skill or plugin tests in addition to the repository validator.
- Use a feature branch named `users/<github-login>/<short-task>` and open a
  pull request to `main`.
- In the pull request, summarize the capability, changed paths, validation, and
  risks or follow-up.
- Do not merge without human review. Delete the feature branch only after the
  pull request is confirmed merged.
