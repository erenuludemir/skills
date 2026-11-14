# Operational policy and boundaries

- Scope: only explicit authorized local project roots, passed as `--repo`; do not search wallet directories or private documents by default.
- Integrity: reference files are immutable; originals retained, updates additive, hash-verified, and recorded in manifest. Avoid bulk overwrite or deletion.
- Autonomy: observe → assess → plan → evidence → verify; autonomy excludes privileged service repair and all live financial mutations.
- Determinism: bounded subprocess timeouts; no shell expansion; explicit command argument arrays; minimal access; no dependency on Docker.
- Secrets: never display/store wallet seed, API keys, RPC cookies, `bitcoin.conf`, or `.env` values. Tool and process presence only.
- Bitcoin Core: optional bounded `bitcoin-cli getblockchaininfo` only when caller deliberately supplies `--bitcoin-cli` and `--bitcoin-datadir`. No wallet RPC calls. Report node synchrony from observed `initialblockdownload` and `verificationprogress`; never assume sync from CLI existence.
- Repairs: no direct modification in this version. Plans must enumerate preconditions, expected diff, approval, rollback and post-checks.
- Runtime: ensure launchd service only runs read-only observations; remove only via an explicit uninstall action and never delete historical reports.
- NVIDIA source: upstream catalog terms retained in archived README; this custom QuantumAI skill is NOT endorsed or signed by NVIDIA.
