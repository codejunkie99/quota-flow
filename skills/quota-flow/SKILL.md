---
name: quota-flow
description: Implement features, fix bugs, create skills, and verify deliverables with Astra orchestration, Sol implementation, and narrowly scoped DeepSeek V4.1 Flash and Luna subagents while minimizing avoidable usage.
---

# Quota Flow

Optimize **usage per accepted deliverable**, including orchestration, reasoning,
retries, and verification. Preserve correctness and the user's scope. This is an
adaptive workflow, not a guarantee of minimum billing or universal correctness.

## Roles and startup

- **Astra orchestrates:** define acceptance, assign ownership, resolve material
  ambiguity, integrate evidence, and report. Keep its turns short; do not repeat
  a worker's investigation or implementation.
- **Sol implements:** own substantial edits, feature work, bug fixes, and skill
  authoring. Start at medium effort; use high for difficult logic or a failed
  approach with an identified reasoning gap. Reuse the same implementation agent.
- **DeepSeek V4.1 Flash supports:** bounded discovery, log reduction, reproductions,
  existing test execution, and mechanical checks. No open-ended architecture.
- **Luna supports:** independent acceptance checks, focused diff review, edge-case
  analysis, and checking generated skills. Start at low effort. Implementation
  findings go back to Sol, rather than creating another implementation owner.

Use only the roles needed. The default is **Astra → Sol → existing checks → done**.
Flash and Luna are optional. Terra is not part of this configuration. This skill
explicitly requests bounded subagent delegation under these roles.

At first use, inspect the available agent names and current model. Read
[runtime.md](references/runtime.md) only when resolving routes or launch settings.
Prefer the installed `quota_sol`, `quota_sol_deep`, `quota_flash`, and
`quota_luna` profiles. Verify effective model/provider/effort from runtime evidence
where exposed; a model name in an agent's answer is not verification.
If the root is not Astra, disclose it and provide the launch/switch instruction;
never claim a skill changed the running root model. Do not silently substitute a
different model when a required route is unavailable. Complete independent work
that remains possible and report the route blocker.

## Execute the smallest sufficient workflow

1. **Define done.** Extract the requested outcome, protected behavior, relevant
   files/artifacts, and observable acceptance checks. Resolve only uncertainty
   that would change the result. Skip ceremonial planning for obvious tasks.
2. **Inspect once.** Use targeted tools directly when enough. Delegate a Flash
   discovery packet only if it saves substantial Astra/Sol context or can run
   independently alongside useful work. Retrieve exact sources before editing.
3. **Give Sol one owned work packet.** Include goal, constraints, starting state,
   relevant paths, checks, and known failures. Let it implement and run the checks
   within its own turn; do not route every shell result through Astra. Sol may
   batch tightly related changes. One writer per overlapping file set.
4. **Verify at the right level.** Existing tests, schema checks, builds, runtime
   inspection, and artifact inspection precede optional model review. Use a fresh
   Luna pass when independent judgment adds value: changed contracts, tricky
   edge cases, or reusable skill behavior. Review the actual final artifact/diff.
5. **Loop only on actionable evidence.** Send Sol the failing assertion, observed
   behavior, or source-linked finding. Preserve its context and test only what
   the change invalidates. Stop when acceptance is met and required checks pass.

For a trivial answer or a non-semantic edit completely resolved by a deterministic
tool, skip worker orchestration. This exception does not authorize Astra to take
over substantive implementation.

## Progress-aware loop

Keep one compact state record for multi-step or interrupted work, in an existing
task record or `work/quota-flow-state.md`. Do not create one for trivial tasks.
Record acceptance, current owner, last artifact/check result, unresolved failure,
next action, loop count, and any explicit user budget. Read it when resuming.

Each repair cycle must add a changed hypothesis, a targeted change, or new
evidence. After **two consecutive cycles on the same failure without progress**,
Astra diagnoses once: missing input/environment → concrete blocker; insufficient
reasoning → Sol high; incorrect requirement → resolve the ambiguity. Do not reset
the counter by renaming the task or spawning a fresh agent. After that intervention,
another no-progress cycle ends this repair branch with a precise blocker and saved
state; continue independent authorized work. Never call a blocked branch complete.
Progressing work may continue to completion within the user's budget.

Honor explicit token, time, or call limits across parent and children. If a limit
cannot be measured/enforced, say so before treating it as a hard guarantee. At a
known budget boundary, save state and report incomplete work instead of claiming
success. Do not invent an overall task budget or purchase/reset quota. A loop runs
in the current task; future scheduled work requires an actual scheduling tool and
the user's request. Do not promise background work after the turn ends.

## Keep the overhead small

- Default to one active worker; allow at most two for disjoint, useful work.
  Parallelism reduces latency, not necessarily usage. Workers must not spawn
  further workers. Tell them they share the workspace and must preserve others' edits.
- Pass a compact standalone packet with file pointers and necessary excerpts.
  Prefer no history fork where supported. Never omit required constraints merely
  to meet a token target. Preserve relevant decisions across handoffs.
- Aim for worker returns under 250 words: outcome, changed paths, actual checks,
  failures, next action. Keep verbose logs in local artifacts and cite them.
- Reuse completed exploration and accepted plans. Run independent tool reads in
  batches; use event-driven waits; do not repeatedly poll unchanged work.
- No automatic all-model chain, reviewer committee, recursive delegation, or
  always-max reasoning. Raise effort only for a specific unmet need.
- Usage is provider/account specific. Cached or estimated tokens are not free
  quota. Check available usage once at start/end only when useful; do not spend
  premium calls maintaining a verbose usage diary.

## Task adapters

Read [task-adapters.md](references/task-adapters.md) only for the relevant task:
bug fixes, features/refactors, skill/slash-command creation, or non-code artifacts.
Retain the same roles, acceptance criteria, and loop semantics for every adapter.

Finish with the delivered result, verification, and remaining limitations. Include
the actual model route and usage only if available or requested. Never invent
quota savings, model identity, test success, or publication state.
