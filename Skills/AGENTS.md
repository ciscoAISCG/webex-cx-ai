# AI SCG standalone skill instructions

These instructions apply to standalone contributions under `Skills/`. The root
`AGENTS.md` instructions also apply. All paths below are relative to the
repository root.

## Confirm the destination

- Use this folder only when the user explicitly wants a standalone,
  manually-installed skill.
- If the capability should be distributed through the AI SCG Plugin
  Marketplace, stop and follow `Plugins/AGENTS.md` instead.
- Do not publish the same skill in both `Skills/` and `Plugins/`.

## Build or update the skill

- Use the built-in skill-creation workflow when available, but treat this
  repository contract and `scripts/validate_contributions.py` as authoritative.
- Create new skills under `Skills/<skill-name>/SKILL.md` with a lower-case,
  hyphenated name.
- Include concise `name` and trigger-oriented `description` frontmatter.
- Keep only scripts, references, agents metadata, and assets that the workflow
  actually needs.
- Preserve the existing folder and skill identity when updating an existing
  skill.
- Add a new standalone skill to the table in `Skills/readme.md`.
- From the repository root, run `python3 scripts/validate_contributions.py` and
  all skill-specific tests before preparing the pull request.
