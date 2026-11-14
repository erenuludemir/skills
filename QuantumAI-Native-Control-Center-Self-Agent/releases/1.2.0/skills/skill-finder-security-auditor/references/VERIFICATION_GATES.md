# Evidence / readiness matrix
- G0 scope & provenance: explicit target and source URLs; UNKNOWN when unobserved.
- G1 prerequisites: Node >=22.20.0, npx, git. FAIL when absent or old.
- G2 source audit: inventory, hashes, review of SKILL.md/scripts, external network/secret risk; suspicious cases BLOCKED until reviewed.
- G3 installation authorization: specific written approval for selected third-party skill (not implicit in browsing request); BLOCKED without approval.
- G4 install execution: authorized desktop/terminal only; no overwrite/delete; record exit code and before/after hashes.
- G5 verification: expected `SKILL.md`, regular file with `--copy`, CLI global list + Claude Code new-session integration where available.
- G6 production: mark PASS only after G0–G5 succeed and real host behavior/permissions are demonstrated. No skill package or ChatGPT plugin by itself grants remote shell privileges.
- GitHub CI and host statuses are independent. An inherited Verify Authors FAIL remains FAIL until legitimate policy procedure or authorized exemption; do not falsify author.
