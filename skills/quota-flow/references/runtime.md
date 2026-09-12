# Runtime and route resolution

The shipped routes were matched to an installed Codex 0.153.4 catalog on
2026-09-12. Catalog presence is not entitlement or a successful request. Recheck
on a different installation. Never copy credentials, machine paths, or account
configuration into the shared skill.

| Role | Profile | Model | Effort |
|---|---|---|---|
| Root orchestration | CLI launcher / model picker | `gpt-6-astra` | low |
| Implementation | `quota_sol` | `gpt-5.6-sol` | medium |
| Difficult implementation | `quota_sol_deep` | `gpt-5.6-sol` | high |
| Bounded support | `quota_flash` | `opencode-go/deepseek-v4.1-flash` | high (catalog-supported) |
| Acceptance/review support | `quota_luna` | `gpt-5.6-luna` | low |

Flash uses `model_provider = "codex-router"`; the other profiles explicitly use
`openai` so they do not inherit a third-party provider from the parent. These are
route choices, not a statement of comparative benchmark performance or quota cost.
The repeated version string `v4.1.4.1` is not a separate verified model.

Use the exact custom-agent name offered by the current spawn schema. Installed
profiles pin model and effort and can override spawn arguments. Never use a
similarly named role without inspecting its actual route. New roles may require a
fresh task. If a role is absent, an explicitly supported model/provider override
may work; if the tool cannot express the required route, report the limitation.
Do not start nested CLI sessions as an automatic workaround.

If the runtime supports `fork_turns`, use `"none"` plus a complete packet. Other
harnesses may expose a different option; follow the live schema, not invented keys.
Use follow-up on the same Sol agent for repairs. For a reasoning upgrade, use a
supported update; otherwise use `quota_sol_deep` once with the current diff, compact
state, checks, and the unresolved hypothesis. Stop the previous writer first.

The CLI launcher starts Astra at low effort and standard service tier for that
session. It does not change global configuration or buy credits. The desktop
skill/prompt cannot change the current root or service tier: choose Astra/Low and
standard speed in the UI if supported. Users can choose higher effort when needed.

## Usage evidence

Track actual provider quota buckets separately. OpenAI-family models may share
account limits; switching among them does not create fresh allowance. Flash can
consume a separate subscription/provider limit, but confirm the route and meter.
Output length and reasoning settings are levers, not exact quota multipliers.
The workflow's call/loop rules are prompt instructions, not a billing firewall.

For calibration, compare a small set of representative completed tasks against
Astra alone or the previous workflow, holding acceptance tests and starting state
fixed. Include orchestration, input, cached input, output, reasoning (when reported),
retries, wall time, and final acceptance. Report native usage deltas only when
concurrent account activity and window resets can be excluded. Keep unreported
values unknown. Tune from repeated accepted outcomes, not one fast run.

## Compact delegation packet

```text
Goal / observable acceptance:
Owned files or read-only scope:
Starting state / relevant paths and excerpts:
Constraints / preserved behavior / existing user edits:
Checks to run / exact failure already observed:
Stop or escalation condition / explicit user budget if any:
Return: result, paths, actual check outcomes, blockers. Aim for <=250 words.
You share this workspace. Preserve other edits. Do not spawn agents.
```
