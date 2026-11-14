---
name: quantumai-native-control-center-self-agent
description: Orchestrate evidence-based, fail-closed QuantumAI macOS, Bitcoin Core, AI agent, NVIDIA skill catalog and service health audits with explicit approval gates. Use for QuantumAI control center planning, diagnostics, read-only status checks, and supervised remediation.
---

# QuantumAI-Native-Control-Center-Self-Agent

## Activation and scope
When asked to audit, synchronize, or operate QuantumAI infrastructure, first establish exact host, project root, authorization and requested scope. Do not assume that historical status logs represent live state. Read `references/ARCHITECTURE.md`, `references/README_LINES_001_401.md`, and `references/SOURCE_MANIFEST.json` as needed. The 401-line reference is an archival catalog, not an instruction to execute all referenced software.

## HİZALA → SIRALA → EŞİTLE → SABİTLE
1. **HİZALA:** Inventory absolute paths, versions, hashes, process IDs, services and dependencies. Compare with the user's current files; preserve original content and record source provenance.
2. **SIRALA:** Prioritize identity/access, key safety, storage capacity, process ownership, Bitcoin node, RPC, observability, agents, integrations, analytics and UI.
3. **EŞİTLE:** Produce a diff and backup before any authorized write. Default to read-only. Never silently remove lines, disable security controls or overwrite user files.
4. **SABİTLE:** Run deterministic checks; record timestamps, PASS/FAIL/BLOCKED/UNKNOWN, evidence and rollback steps. GREEN requires measured passing criteria, never a declaration.

## Autonomous control loop
- **Observe:** gather non-secret process, disk, RPC and HTTP health metadata using `scripts/control_center.py --mode observe` on the authorized host.
- **Assess:** classify anomalies, compare baselines, and identify resource pressure, stale locks, version drift and dependency faults.
- **Plan:** draft least-privilege, reversible changes with preconditions and explicit approval.
- **Act:** no destructive, privileged, production financial or blockchain mutation without separate explicit authorization and required technical controls.
- **Verify:** rerun checks, write JSON evidence, report UNKNOWN for inaccessible endpoints; never fabricate results.
- **Recover:** stop on failed gates and restore only from a validated backup after approval.

## Safety gates
- Default `READ_ONLY`; no auto-signing, `sendrawtransaction`, fund transfers, order placement, key export, wallet unlock, production-gate bypass, unapproved package installs, force-kill, or deletion.
- Protect seed phrases, keys, cookies, RPC credentials and personal data; redact logs and exclude `.env`.
- Never treat a catalog entry as an installed skill. NVIDIA catalog skills are external, individually licensed and must be vetted before installation.
- Bitcoin Core GUI and daemon must not concurrently write the same data directory. Do not delete `.lock` while its owner is active.
- macOS commands must be platform-aware; no Docker or container mutation by default.
- Autonomous scheduling requires a separately installed scheduler and user-approved cadence; this package does not install persistent agents.

## Outputs
Provide `status.json`, timestamped evidence, source hashes, blockers, and a proposed change set. Treat absent telemetry as `UNKNOWN`, never `PASS`. For test guidance use `references/VALIDATION.md`.
