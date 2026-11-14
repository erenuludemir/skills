# GitHub implementation / installation

This is a self-contained GitHub-friendly skill and workflow scaffold. Import the `QuantumAI-Native-Control-Center-Self-Agent` directory into your own project; copy `workflow-readonly-audit.yml` into `.github/workflows/quantumai-readonly-audit.yml` (create only if missing). The workflow runs unit validation and writes a non-secret report; no deployment and no financial transaction.

Recommended external clone:
`git clone --depth=1 https://github.com/erenuludemir/skills.git`

The upstream repo is the NVIDIA catalog mirror; do not replace its existing CI or NVIDIA marketplace identity. Add any integration through a dedicated branch and PR, not as a destructive in-place overwrite.
