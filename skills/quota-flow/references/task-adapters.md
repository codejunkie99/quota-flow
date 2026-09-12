# Task adapters — read only the relevant section

## Bug fix

Get a reproduction or a precise observed failure. Flash can isolate the failing
test or summarize logs; Sol diagnoses and fixes the root cause. Preserve adjacent
behavior. Add a regression test when it meaningfully protects the bug, then run
affected checks. If reproduction is impossible, state the gap and distinguish a
plausible patch from a verified fix. Treat missing services, permissions, and
dependencies as environment failures, not reasons to keep changing code.

## Feature or refactor

Identify interfaces, callers, invariants, and acceptance before broad edits. Sol
owns the coherent implementation slice and integrates it. Split a large task into
acceptance-bearing milestones; each completed milestone should leave a usable
state. Luna reviews risky contract changes or hidden edge cases once; Sol addresses
actionable findings. Repeat review only where a change invalidates earlier evidence.
Repository-required checks remain required even when they are expensive.

## Skill or slash-command creation

Sol is the author. Read the environment's available skill-creator instructions
just in time; do not paste another full workflow into every task. Create concise
`SKILL.md` frontmatter and a short decision-changing entrypoint; put conditional
details in references. Add scripts only for useful deterministic operations.

Preserve the user's requested model roles, approvals, scope, and invocation mode.
A generated skill grants no new authority to send messages, publish, delete, or
spend. Keep repeated failures as narrow fixes rather than accumulating universal
rules. Do not rewrite this orchestration skill unless the user requests it.

Validate structure using the installed validator if available. Exercise scripts
with meaningful failure cases. Luna can forward-test realistic scenarios using
only the skill and raw task, without being told the intended answer. Include a
trivial task, incomplete requirements, repeated failure, unavailable model, and
a task requiring independent artifact verification when appropriate.

For Codex use `$skill-name` as the portable invocation. If a slash command is
requested, ship a thin custom prompt in the supported prompt directory; do not
duplicate the skill. Escape a literal dollar as `$$` in a Codex custom prompt.
Document that `/prompts:name` is a deprecated CLI/IDE compatibility path, and
verify actual client discovery before claiming the command appeared in the UI.

## Non-code deliverable

Sol produces the requested artifact with appropriate domain tools; Flash gathers
bounded evidence and Luna checks acceptance when useful. Use available specialist
skills only when relevant. Verify content and rendered output where appropriate.
Do not force code tests onto prose, research, design, or media. Missing tools or
domain evidence are explicit limitations, not permission to fabricate output.
