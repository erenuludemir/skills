# QuantumAI / Skill Finder v1.2.0 (additive release)
Existing v1.1.1 control-center and historical references remain unchanged; new skill `skill-finder-security-auditor` and `integrations/macos/install_find_skills.zsh` are added.

## Scope
1. Discover on skills.sh, search exact tasks, rank by installs/publisher/GitHub stars.
2. Audit source filenames/hash/script risks without execution or arbitrary network downloads.
3. Enforce Node >=22.20.0; preserve existing installations; verify Claude Code copy installation.
4. Explicit install authorization remains separate. Offline library tests cannot establish production readiness.

Run `python3 -m unittest discover -s skills/skill-finder-security-auditor/tests -v` from plugin root. Existing `scripts/validate_skill.py` and QuantumAI tests remain applicable.

Upstream: Vercel skills/find-skills/SKILL.md, source blob `a41bdd074bb587afd861332cf2f473f3154de4d7`, attribution preserved. No claim of Vercel endorsement.
