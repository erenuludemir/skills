# Validation
1. Verify original file SHA-256 matches `SOURCE_MANIFEST.json`.
2. Verify archival reference first 400 lines match original and line 401 is empty.
3. Run `python3 scripts/control_center.py --mode observe` on macOS; unknown or missing dependencies must not become PASS.
4. Run `python3 scripts/validate_skill.py` for offline structural and provenance tests.
5. Do not report host deployment or persistent automation until independently verified on the host.
