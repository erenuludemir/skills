---
name: quantumai-native-control-center-self-agent
description: Execute evidence-driven, fail-closed QuantumAI macOS and Bitcoin Core observations, agent health checks, source-integrity audits, GitHub repository inventory, reversible remediation planning and verified automation lifecycle. Use to align, prioritize, synchronize, and freeze QuantumAI control-center workflows without data loss.
---
# QuantumAI-Native-Control-Center-Self-Agent

## Contract: HİZALA → SIRALA → EŞİTLE → SABİTLE
1. **HİZALA** — Locate actual absolute paths, inventory existing content and compare tracked Git state, SHA-256, process owners, disk, services, Node RPC and agent health. Never infer live state from text archives.
2. **SIRALA** — Dependency-aware DAG: authorization → storage → source integrity → identity/keys → active process ownership → blockchain/RPC → agent runtime → integrations → analytics/UI → reporting. Determine prerequisites and current desired state.
3. **EŞİTLE** — Derive non-destructive changes from **full original files**. Maintain originals verbatim, create sidecar versions, compare diffs, require validated backups for every authorized live modification. No silent pruning or omissions.
4. **SABİTLE** — Run executable verification and store evidence; issue PASS only for measured acceptance criteria, otherwise FAIL / BLOCKED / UNKNOWN. Keep proof and rollback instructions.

## Multi-agent orchestration
`Supervisor → Observer → Carrier → Organizer → Preparer → Worker → CodeCompletion → ReverseAnalysis → Validator → DecisionAI → Reporter`
Each step persists a typed artifact; no stage may skip a failed prerequisite. The Supervisor can rerun failed **read-only** observations, while requiring distinct approval for writes or service disruption. The Worker cannot self-upgrade authorization.

## Commands
- `python3 scripts/control_center.py observe --repo /absolute/path/to/repository --output /absolute/path/to/status.json`
- `python3 scripts/control_center.py plan --repo /absolute/path/to/repository --output /absolute/path/to/plan.json`
- `python3 scripts/control_center.py verify --repo /absolute/path/to/repository --output /absolute/path/to/verification.json`
- `python3 scripts/control_center.py report --repo /absolute/path/to/repository --output /absolute/path/to/report.json`
- `python3 scripts/validate_skill.py --root .`
- `python3 -m unittest discover -s tests -v`
All above commands remain non-destructive. They do not require Docker or external Python dependencies.

## Github and upstream provenance
The user repository `erenuludemir/skills` is a fork or mirror of the NVIDIA Agent Skills catalog, NOT automatically a QuantumAI implementation. The uploaded `README.md` is retained byte-identically as `references/UPSTREAM_README_ORIGINAL.md`, with 400 physical lines. Its 401-line archival version appends one empty physical line without modifying the first 400. GitHub clone and source-tree inventory are separately evidenced; access to files does not imply audit of every source line or cryptographic verification of every upstream skill.

## Fail-closed policies
- Default `READ_ONLY`, no key material disclosure, wallet unlock, order placement, RPC broadcasting, chain reorg alteration, live payment, or financial transfers. Approval must never bypass independent credential, authorization, network, balance, compliance, and hardware-wallet controls.
- Never delete a Bitcoin Core `.lock` if its PID has the lock; never launch daemon and GUI against the same database simultaneously.
- No unapproved installs, Docker mutations, `sudo`, `rm -rf`, force kill or modification of system LaunchAgents. Never overwrite or remove user lines without an explicit reversible, reviewed migration.
- NVIDIA signatures are theirs, not ours. Never claim NVIDIA verification or generate a fake `.oms.sig`; record own SHA-256 only. A catalog reference is not an installed skill.
- Report current machine `UNKNOWN` until direct target-host evidence exists. Code and unit tests cannot establish production readiness alone.

## Runbook references
Read `references/ARCHITECTURE.md`, `references/OPERATIONAL_POLICY.md`, `references/REPOSITORY_AUDIT.md`, `references/VALIDATION.md` and `references/SOURCE_MANIFEST.json` when relevant. Also review `references/README_LINES_001_401.md` on catalog-related tasks. Use `integrations/macos/install_launchagent.sh` only for opt-in local hourly **read-only** observation. Use `integrations/github/` for GitHub Actions CI; never auto-merge into `main`.


## Host-verified extension — v1.1.1 (2026-11-12)
- The linked GitHub repository was cloned to the authorized macOS host. A full tracked-file content read and SHA-256 scan covered 6,780 files on the isolated feature branch, with zero read errors. Read `references/HOST_STATIC_AUDIT_2026-11-12.json` and `references/COMPLETE_SOURCE_INTEGRATION_POLICY.md`. Scan coverage **does not** imply that every skill was executed or audited for semantic vulnerabilities.
- `scripts/audit_repository.py` provides a repeatable, repository-nonmutating SHA-256 inventory and checks direct child `skills/*/SKILL.md` headers and signature filenames. It never claims to cryptographically validate NVIDIA OMS signatures.
- GitHub PR #1 and workflow evidence: `references/GITHUB_PR_CI_EVIDENCE_2026-11-12.json`. The existing NVIDIA-derived author verification policy remains a legitimate failing gate; never change author identity or bypass policy to claim PASS.
- The hourly macOS LaunchAgent was installed and its read-only report observed. The report's overall state is UNKNOWN, while financial production/broadcast is BLOCKED; read `references/MACOS_DEPLOYMENT_EVIDENCE_2026-11-12.json`.
- Keep all historical evidence and do not silently overwrite source. Additional observation may improve coverage, but agent self-approval cannot enable live transactions or production authority.
