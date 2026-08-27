# AI SCG marketplace plugin instructions

These instructions apply to `Plugins/` and
`.agents/plugins/marketplace.json`. The root `AGENTS.md` instructions also
apply. All paths below are relative to the repository root.

## Build or update the package

- Use the built-in plugin-creation workflow when available, but treat this
  repository contract and `scripts/validate_contributions.py` as authoritative.
- Create plugins under `Plugins/<plugin-name>/` using a stable, lower-case,
  hyphenated name.
- Every plugin must include `.codex-plugin/plugin.json` with the same `name`, a
  valid semantic `version`, an AI SCG author, and complete interface metadata.
- Put bundled skills under `Plugins/<plugin-name>/skills/<skill-name>/SKILL.md`.
- A plugin may contain one skill, multiple skills, an MCP server, an app, or a
  supported combination.
- Include only files required by the plugin. Preserve existing assets and avoid
  duplicating a standalone copy under `Skills/`.

## Register and release

- For a new plugin, add exactly one matching entry to
  `.agents/plugins/marketplace.json` with a `./Plugins/<plugin-name>` source.
- Add a new plugin to the table in `Plugins/README.md`.
- Give every plugin a `README.md` with an `Installation` section containing a
  copyable natural-language Codex prompt. Make Codex perform the technical
  installation and state only unavoidable human actions such as protected
  approvals, browser authentication, or restart.
- Make every installation section tell the user to set the Codex task
  permission to `Ask for Approval`. The copyable prompt must check whether
  protected-write approval is available and, when it is not, stop with that
  exact instruction instead of suggesting `sudo`, permission changes, or other
  workarounds.
- Link every plugin README to the canonical consumer update instructions at
  `../README.md#update-my-plugins`.
- For an update, preserve the folder, manifest name, and marketplace identity.
  Update the contents and increment the manifest version; never create a
  numbered replacement folder.
- Do not add another marketplace entry for an existing plugin release.
- From the repository root, run `python3 scripts/validate_contributions.py` and
  all plugin-specific tests before preparing the pull request.
