# Research and design

## Source inspection
- The supplied `README.md` is the NVIDIA Agent Skills catalog mirrored in `erenuludemir/skills` (GitHub connector verified `README.md` on default branch); it is not a QuantumAI runtime implementation.
- Local uploaded README has **400 physical lines**. `README_LINES_001_401.md` retains all 400 original lines byte-for-byte and adds an empty line 401; no content is invented for line 401.
- Git clone was attempted but blocked by DNS in the execution container. The remote README was independently sampled through the GitHub connector; the entire remote tree was not cloned or audited.
- Additional supplied text contains historical operational logs, not verified live status. It is intentionally not executed.

## Architecture
Supervisor → Inventory → Security Gates → Node/RPC → Agent Health → Service Health → Analytics → Evidence Store → Human Approval → Reversible Remediation.

## Status contract
`PASS`: evidence meets explicit criteria; `FAIL`: tested and failed; `BLOCKED`: denied by policy or prerequisites; `UNKNOWN`: no trustworthy measurement.

## Deployment
Copy the skill directory into a supported agent's skills directory. Run `python3 scripts/control_center.py --mode observe --output /tmp/qai-status.json` on the intended macOS host. Review output before enabling any external automation. No background daemon is installed by this package.
