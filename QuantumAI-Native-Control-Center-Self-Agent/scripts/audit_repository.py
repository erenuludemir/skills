#!/usr/bin/env python3
"""Hash every tracked file in an authorized Git repository without executing code."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

def git(repo, *args):
    return subprocess.run(['git','-C',str(repo),*args],capture_output=True,check=True).stdout

def audit(repo):
    p=Path(repo)
    if not p.is_absolute():
        return {'status':'BLOCKED','reason':'Repository must be an absolute path'}
    if not p.is_dir():
        return {'status':'FAIL','reason':'Repository missing'}
    try:
        top=Path(os.fsdecode(git(p,'rev-parse','--show-toplevel')).strip())
        commit=git(p,'rev-parse','HEAD').decode('ascii').strip()
        paths=[os.fsdecode(v) for v in git(p,'ls-files','-z').split(b'\0') if v]
    except (subprocess.CalledProcessError,OSError,UnicodeError) as exc:
        return {'status':'FAIL','reason':type(exc).__name__}
    aggregate=hashlib.sha256()
    counted_bytes=0
    read_count=0
    missing_signatures=[]
    invalid_frontmatter=[]
    read_errors=[]
    skfiles=[]
    signatures=[]
    for name in paths:
        f=top/name
        try:
            if f.is_symlink():
                blob=os.fsencode(os.readlink(f))
            else:
                blob=f.read_bytes()
            read_count+=1
            counted_bytes+=len(blob)
            aggregate.update(os.fsencode(name)+b'\0'+hashlib.sha256(blob).hexdigest().encode()+b'\n')
            if name.startswith('skills/') and name.endswith('/SKILL.md') and name.count('/')==2:
                skfiles.append(name)
                raw=blob[:16384].decode('utf-8','replace')
                if not (raw.startswith('---\n') and '\nname:' in raw and '\ndescription:' in raw):
                    invalid_frontmatter.append(name)
            if name.startswith('skills/') and name.endswith('/skill.oms.sig') and name.count('/')==2:
                signatures.append(name)
        except (OSError,ValueError) as exc:
            read_errors.append({'path':name,'error':type(exc).__name__})
    signature_set=set(signatures)
    for name in skfiles:
        expected=name.rsplit('/',1)[0]+'/skill.oms.sig'
        if expected not in signature_set:
            missing_signatures.append(name)
    valid=not(read_errors or invalid_frontmatter or missing_signatures)
    return {'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'operation':'full-static-read-and-sha256',
            'execution_mode':'READ_ONLY_FOR_REPOSITORY',
            'status':'PASS' if valid else 'FAIL',
            'repository_absolute_path':str(top),
            'commit':commit,
            'tracked_files':len(paths),
            'readable_files':read_count,
            'total_bytes_read':counted_bytes,
            'path_content_sha256':aggregate.hexdigest(),
            'root_skills':len(skfiles),
            'root_signature_filenames':len(signatures),
            'missing_signature_filenames':missing_signatures[:50],
            'invalid_skill_frontmatter':invalid_frontmatter[:50],
            'read_errors':read_errors[:50],
            'signature_cryptographic_validation':'NOT_PERFORMED',
            'semantic_review_and_production_readiness':'NOT_PROVEN'}

def main(argv=None):
    pa=argparse.ArgumentParser()
    pa.add_argument('--repo',required=True)
    pa.add_argument('--output',default=None,help='Optional absolute JSON evidence location, outside repository')
    args=pa.parse_args(argv)
    result=audit(args.repo)
    payload=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output:
        dest=Path(args.output)
        if not dest.is_absolute() or not dest.parent.is_dir():
            pa.error('--output must use an absolute path with existing parent directory')
        try:
            dest.relative_to(Path(args.repo).resolve())
            pa.error('--output must not modify the audited repository')
        except ValueError:
            pass
        temp=dest.with_name(dest.name+'.tmp.'+str(os.getpid()))
        with temp.open('x',encoding='utf-8') as fp:
            os.chmod(temp,0o600)
            fp.write(payload)
        os.replace(temp,dest)
    print(payload,end='')
    return 0 if result['status']=='PASS' else 2

if __name__=='__main__':
    sys.exit(main())
