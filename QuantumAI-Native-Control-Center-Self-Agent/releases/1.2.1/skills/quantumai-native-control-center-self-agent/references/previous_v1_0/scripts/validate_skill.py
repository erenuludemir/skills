#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parents[1]
m=json.loads((r/'references/SOURCE_MANIFEST.json').read_text())
a=(r/'references/UPSTREAM_README_ORIGINAL.md').read_bytes()
b=(r/'references/README_LINES_001_401.md').read_bytes()
assert hashlib.sha256(a).hexdigest()==m['original_sha256']
assert len(a.splitlines())==400
assert b==a+b'\n'
assert len(b.split(b'\n'))==402
assert (r/'SKILL.md').read_text().startswith('---\n')
print('PASS: provenance, 400 original lines + blank line 401, skill metadata')
