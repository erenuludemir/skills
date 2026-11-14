#!/usr/bin/env python3
"""Local integrity verification for this independently authored skill."""
import argparse, hashlib, json, pathlib, re, sys

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--root',default=None)
    a=p.parse_args(argv)
    root=pathlib.Path(a.root).resolve() if a.root else pathlib.Path(__file__).resolve().parent.parent
    checks={}
    meta=(root/'SKILL.md').read_text(encoding='utf-8')
    checks['frontmatter']=meta.startswith('---\n') and bool(re.search(r'^name: quantumai-native-control-center-self-agent$',meta,re.M)) and 'description:' in meta
    origin=(root/'references/UPSTREAM_README_ORIGINAL.md').read_bytes()
    archived=(root/'references/README_LINES_001_401.md').read_bytes()
    sha=hashlib.sha256(origin).hexdigest()
    checks['original_sha256']=sha=='d384e899b451e53e73ae9113744e7612b1d2ced534ce807b833333bf234e8be3'
    checks['original_400_lines']=len(origin.splitlines())==400
    checks['archive_401_lines']=archived==origin+b'\n' and len(archived.splitlines())==401
    checks['source_manifest']=json.loads((root/'references/SOURCE_MANIFEST.json').read_text())['uploaded_readme_sha256']==sha
    mandatory=('references/REPOSITORY_AUDIT.md','references/OPERATIONAL_POLICY.md','integrations/github/workflow-readonly-audit.yml','integrations/macos/install_launchagent.sh','tests/test_control_center.py','skill-card.md')
    checks['required_files']=all((root/m).is_file() for m in mandatory)
    checks['no_fake_nvidia_signature']=not (root/'skill.oms.sig').exists()
    print(json.dumps({'PASS' if all(checks.values()) else 'FAIL':checks},indent=2))
    return 0 if all(checks.values()) else 1
if __name__=='__main__':sys.exit(main())
