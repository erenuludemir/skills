# Architecture and research — 2026-11-12

## Sources and truth boundaries
- Uploaded 400-physical-line NVIDIA catalog README; archived copy with one added blank line 401.
- Remote default-branch Git tree obtained with authenticated GitHub connector at `d59805503396547363ff0079c436b1cae496e1af` (9,081 entries: 6,752 blobs and 2,329 trees, untruncated). The full Git repository was **successfully cloned to an authorized macOS host**, and its 6,752 tracked files were enumerated. This establishes repository acquisition/inventory, NOT code review of every file.
- GitHub catalog snapshot has 451 `SKILL.md` paths and 451 `skill.oms.sig` paths. Presence does not prove individual signature validity.
- Uploaded README is NVIDIA-derived catalog: do not misidentify it as a working QuantumAI runtime.

## Dependency graph
Source integrity / storage / authorization → observed processes → Bitcoin Core and RPC diagnostics → agent service probes → runbook candidate generation → diff / tests → approval-based changes → verification → status report. There is NO automatically deployed self-healing production system in this artifact.

## Agency roles
Supervisor controls deterministic DAG and audit evidence; Observer collects resource metrics; Carrier maps component adapters; Organizer resolves dependency order; Preparer lists necessary setup; Worker executes only separately-approved non-financial local changes; CodeCompletion may suggest patches without applying them; ReverseAnalysis compares expected and observed results; Validator tests; DecisionAI assigns severity, not authority; Reporter emits JSON.

## Status contract
`PASS`: observed condition meets specified evidence; `FAIL`: tested and mismatch; `BLOCKED`: gate forbids run; `UNKNOWN`: not measured. `READY_FOR_READ_ONLY_AUDIT` is distinct from `PRODUCTION_READY`.

## Machine deployment
Supported macOS deployment script can install a user LaunchAgent for hourly read-only audits if explicitly invoked. The package itself does not claim that launchd installation or host execution has occurred. Production financial gates are deliberately disabled.

## v1.1.1 observed deployment
macOS LaunchAgent loaded (3600 s); source tree content scan PASS for file coverage; actual production finance status BLOCKED. Reference evidence JSON files, not this note, for exact timestamps.
