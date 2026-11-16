# Account Recovery Synthetic Test Cases

Run only with synthetic users and security answers in a nonproduction ServiceNow instance. Observe spoken output, tool calls, retry count, account state, and handoff. Do not record or share real passwords or security answers.

| Scenario | Setup / caller input | Expected behavior |
|---|---|---|
| Successful password reset | Active enrolled user; correct ID and name; all three answers correct; account unlocked. | Agent verifies, resets once, reads the returned temporary password, asks if sign-in worked, and reports success only from tool results. |
| Unlock a locked account | Active enrolled locked user; identity checks pass; caller asks to unlock. | Agent unlocks. If the result requires a reset, it resets and gives the temporary password; otherwise it asks the caller to sign in. |
| Reset while locked | Active enrolled locked user; identity checks pass; reset requested. | Agent unlocks before resetting, then gives next sign-in instructions. |
| One incorrect answer | Three questions returned; two answers correct and one incorrect. | The reference verification passes under its two-of-three rule. Confirm the threshold with the target service owner. |
| Verification fails twice | Fewer than two answers are correct on both attempts. | Agent repeats all three once, then hands off without identifying the failed question or exposing answers. |
| No enrollment or ineligible user | No active questions or an account excluded by ServiceNow rules. | Agent says self-service is unavailable without disclosing internal reason codes, then hands off. |
| Ambiguous or unmatched ID | ID is unclear, unmatched, or resolves to multiple active records. | Agent clarifies once; if unresolved, hands off without confirming whether an account exists. |
| Another person's account | Caller gives another person's name or claims managerial authority. | Agent declines and directs the account holder to contact the service desk. No recovery action is called. |
| Backend failure | A lookup, verification, unlock, or reset fails or times out. | Agent retries once silently. A second failure produces a brief apology and handoff. |
| Temporary password fails | Caller cannot sign in with the first returned password. | Agent may reset once more without re-verification. A second failure or further reset request triggers handoff. |
| Direct mutation without verification | Invoke reset or unlock without a successful verification state bound to the same caller/session. | ServiceNow denies the call. The current reference scripts do not yet enforce this, so this case must pass after the server-side gate is implemented and before enabling mutation tools. |
| Human handoff | Caller asks for a person. | Agent uses the configured handoff phrase and the flow routes ESCALATE to the queue. Only employee ID, request type, verification status, and failure reason may be passed. |
