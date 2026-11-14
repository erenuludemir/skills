# Repository acquisition and inventory

- `https://github.com/erenuludemir/skills.git` — `main` — commit `d59805503396547363ff0079c436b1cae496e1af` — observed 2026-11-12.
- Local full shallow clone on authorized macOS machine: `/Users/erenuludemir/Library/Application Support/QuantumAI-Native-Control-Center-Self-Agent/upstream/skills`.
- GitHub Git tree connector: `truncated=false`, 9,081 paths = 2,329 directories + 6,752 tracked files, 64,005,429 blob bytes by tree metadata.
- macOS host: clone completed (`git clone --depth=1 --single-branch --branch main`), 6,752 tracked files, 93 MiB working directory including `.git`.
- 451 `SKILL.md` files and 451 signature files present by filename inventory, **not verified** against NVIDIA trust anchor.
- Root README `sha256=d384e899b451e53e73ae9113744e7612b1d2ced534ce807b833333bf234e8be3` on authorized Mac, 400 lines; uploaded README must be matched by SHA256 before asserting identity.
- Full contents of 6,752 upstream files are NOT embedded in this relatively small distribution ZIP; the original full clone remains on the connected Mac. The package embeds the full 401-line source and records this source-tree scope accurately.
- Audit scope: every tracked path and Git tree object enumerated; actual inspection of every source file's code, tests, license obligations and signature verification has NOT occurred. Never equate path inventory with complete code audit.

## Follow-up exhaustive file-content hash scan
On the authorized macOS device, every one of the 6,780 tracked files at local feature-branch commit `6912cd457122bd30c3368f8e6dda5cb04046ac76` was opened and SHA-256 hashed (64,180,977 bytes; no read failures). Digest and limitations: `HOST_STATIC_AUDIT_2026-11-12.json`. GitHub PR opened; custom audit CI passed; separate inherited author-verification policy FAIL, not bypassed.
