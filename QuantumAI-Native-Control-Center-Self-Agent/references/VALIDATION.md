# End-to-end verification matrix

1. `python3 scripts/validate_skill.py --root .` — metadata, source hash and 401-line preservation, required files and no false signature.
2. `python3 -m unittest discover -s tests -v` — guardrails, read-only observability, accepted arguments, no mutating actions, status contract and CLI smoke tests.
3. `python3 scripts/control_center.py observe --repo /ABSOLUTE/EXISTING/REPO --output /tmp/qai-observe.json` — target-host evidence; run only after choosing a real absolute path.
4. `python3 scripts/control_center.py plan --repo /ABSOLUTE/EXISTING/REPO` — read-only remediation DAG with no unattended changes.
5. `bash integrations/macos/install_launchagent.sh --dry-run` — only prints deployment plan; opt-in `--install` changes user LaunchAgent and must be run on Mac.
6. `git ls-tree -r --name-only HEAD | wc -l` on upstream clone — compare to `references/SOURCE_MANIFEST.json`.

No test in this ZIP can prove production financial readiness, valid upstream NVIDIA signatures, or installation on an uninspected host. All such claims require direct independent attestation.

## v1.1.1 extended validation
Run `python3 scripts/audit_repository.py --repo /absolute/git/path --output /absolute/evidence.json`. A PASS means every tracked file in that Git checkout was readable and hashed with required root skill file headers and matching signature filenames; it does not verify signature cryptography or system production readiness.
