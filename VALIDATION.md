# Validation — 2026-09-12

## Verified

- The installed skill passes the Codex skill-creator structural validator.
- `python3 -m unittest discover -s tests -v`: **12 tests passed**.
- A native Sol/medium implementation run created the installer and its nine
  filesystem tests. Its focused tests passed.
- A native Luna/low independent inspection found no actionable issues in the
  installer, tests, agent profiles, or launcher. Its `pytest -q` run passed all
  12 tests. This review is bounded evidence, not a correctness guarantee.
- Real user-home installation and `--check` completed successfully. Installed
  files match the shipped source. Existing global configuration was not edited.
- `codex debug prompt-input` includes the installed skill path in a fresh context.
- A Codex 0.153.4 interactive session displayed `gpt-6-astra low` with the launcher
  model/effort settings. The launcher argument tests verify literal task handling.
- Exact model IDs and reasoning levels match the inspected local model catalog.

## Compatibility finding

The installed Codex 0.153.4 CLI rejected `/prompts:quota-flow` as unrecognized.
The deprecated custom-prompt wrapper is shipped only for clients retaining that
feature. **Use `$quota-flow` or the shell launcher on the tested build.** No claim
is made about desktop slash-menu availability. New custom profiles require a
fresh session; their complete end-to-end delegation chain has not been benchmarked.

The optional Flash forward-test did not return its bounded scenario report in a
timely manner and was interrupted to avoid more overhead. No completed Flash
behavioral test is claimed. Its configured route and catalog entry were inspected;
this remains a runtime-validation gap for the full workflow.

## Usage evidence and limits

GitHub publication was verified against the remote commit. The initial GitHub
Actions run ended in `startup_failure` before creating any test jobs; no check-run
diagnostic was exposed by the API. Repository Actions are enabled and the remote
workflow matches the local file. Cloud CI is therefore **not verified passing**;
the 12-test passing result above is local. Initial run:
[34700582018](https://github.com/codejunkie99/quota-flow/actions/runs/34700582018).

Provider-reported totals from the two bounded development runs:

| Run | Input | Cached input (subset) | Output | Reasoning output (reported separately) |
|---|---:|---:|---:|---:|
| Sol installer implementation | 329,446 | 294,784 | 7,661 | 1,893 |
| Luna package inspection | 142,889 | 84,992 | 1,332 | 810 |

These are cumulative provider reports, not quota percentages or billed costs.
Do not add cached input to input or infer reasoning accounting without provider
definitions. Repeated turns and inherited environment context contribute to input.
These are development checks, not a controlled benchmark of this workflow. They
exclude the parent, the optional Flash evaluation, and other development work.

No aggregate quota-saving percentage, exact call-budget enforcement, comparison
against Astra alone, or universally optimal configuration has been established.
The skill provides behavioral routing and stopping rules; it is not a scheduler
or a billing-enforcement service.
