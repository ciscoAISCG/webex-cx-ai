# AI SCG Publication Workflow Test

> This is synthetic test content. It does not represent a customer deployment and contains no customer or tenant data.

## Summary

This playbook verifies the semi-automated publication workflow from `WebexCC-SA/FDE-Engagement` to `ciscoAISCG/webex-cx-ai`.

It uses a minimal scripted digital self-service scenario so that the package satisfies the production playbook metadata contract while remaining safe to test publicly.

A test user sends `publication test`. A synthetic scripted digital AI agent returns:

`The AI SCG publication workflow test is working.`

No API, database, webhook, or external integration is called.

## Owner and maintenance

- Owner: `dbokatov`
- Maintaining team: `fde-team`
- Purpose: Synthetic CI/CD verification
- Revalidation: Required whenever the publication workflow or playbook metadata contract changes

## Applicability

Use this package only to verify the label-gated playbook publication workflow.

It is industry-neutral and uses Chat, Scripted Digital AI Agent, and Self-Service metadata solely to exercise the production taxonomy. It is not a customer implementation guide or production deployment recommendation.

No customer Jira engagement applies because this is a synthetic CI/CD test.

## Prerequisites

- Access to the FDE Engagement repository.
- The `Publish playbook to AI SCG` workflow is present on the `main` branch.
- The AI SCG GitHub App variable and private-key secret are configured.
- The GitHub App is installed for `ciscoAISCG/webex-cx-ai`.
- The source PR validation check can run successfully.
- A reviewer can approve and merge the source PR.

## Implementation

The synthetic scenario has the following logical flow:

1. A test user starts a digital chat.
2. Webex Contact Center routes the interaction to a scripted digital AI agent.
3. The agent matches the synthetic `publication test` message.
4. The agent returns `The AI SCG publication workflow test is working.`
5. The interaction ends without calling an external system.

No Webex tenant configuration or deployable agent artifact is included. The package exists only to exercise repository validation, controlled promotion, catalog generation, and destination PR creation.

## Validation

1. Review this README and `manifest.yaml`.
2. Confirm that the source PR changes only `Playbooks/ai-scg-publication-workflow-test/`.
3. Wait for `Validate playbook metadata and content` to pass.
4. Add the exact `publish:ai-scg` label.
5. Approve and merge the source PR.
6. Open the FDE Engagement Actions page and verify that `Publish playbook to AI SCG` succeeds.
7. Verify that automation creates a draft PR in `ciscoAISCG/webex-cx-ai`.
8. Confirm that the destination PR contains:
   - `Playbooks/ai-scg-publication-workflow-test/README.md`
   - `Playbooks/ai-scg-publication-workflow-test/manifest.yaml`
   - regenerated playbook index and website catalog files
9. Confirm that the destination validation workflow passes.

## Expected result

A draft destination PR is created from a deterministic `automation/fde-pr-*` branch. The PR records the source PR, exact merged commit, publication label, and validation result.

The expected result is a draft destination PR from a deterministic `automation/fde-pr-*` branch. The PR must record the source PR, exact merged commit, publication label, and validation result.

The workflow does not merge the destination PR or publish the test playbook to GitHub Pages automatically.

## Security and privacy

- No customer data is included.
- No credentials, tokens, or private keys are included.
- No tenant identifiers are included.
- No external services are called.
- No customer configuration is included.
- No artifacts are attached.

## Troubleshooting

- If source validation fails, compare `manifest.yaml` with the current AI SCG taxonomy.
- If publication does not start, confirm that the source PR is merged and has the exact `publish:ai-scg` label.
- If token generation fails, verify the GitHub App installation, repository variable, and private-key secret.
- If importing fails, confirm that the source PR changed exactly one playbook package.
- If catalog validation fails, inspect the destination workflow output for an unsupported taxonomy value or generated-site warning.
- If the deterministic destination PR was previously closed without merge, human review is required before another publication attempt.

## References

- [FDE Engagement repository](https://github.com/WebexCC-SA/FDE-Engagement)
- [AI SCG repository](https://github.com/ciscoAISCG/webex-cx-ai)
- [AI SCG playbook taxonomy](https://github.com/ciscoAISCG/webex-cx-ai/blob/main/Playbooks/taxonomy.yaml)
- [Publication workflow](https://github.com/WebexCC-SA/FDE-Engagement/blob/main/.github/workflows/publish-playbook-to-ai-scg.yml)
