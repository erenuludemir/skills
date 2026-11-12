# Locally verified benchmark / tests

Evaluation is limited to bundled, deterministic Python `unittest` tests and source hash checks. This is **not** an NVIDIA Tier-3 benchmark and does not indicate model uplift.

Recorded test outcomes are stored in `references/LOCAL_TEST_RESULTS.json` after package build; reproduced with `python3 -m unittest discover -s tests -v`. All proposed live service repairs remain unexecuted by this unit-test suite.
