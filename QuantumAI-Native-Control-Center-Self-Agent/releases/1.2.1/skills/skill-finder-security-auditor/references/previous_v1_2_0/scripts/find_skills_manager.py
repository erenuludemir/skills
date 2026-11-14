#!/usr/bin/env python3
"""Read-only skill preflight, inspection, and evidence recorder (stdlib only)."""
import argparse, datetime, hashlib, json, os, pathlib, re, shutil, stat, subprocess, sys
MIN_NODE=(22,20,0)
RISK_PATTERNS={
    'remote_shell':r'(?:curl|wget)\b[^\n]{0,240}\|\s*(?:sh|bash|zsh)\b',
    'shell_eval':r'\b(?:eval|exec)\s*(?:\(|[\"\'`$])',
    'destructive':r'\brm\s+-[\w]*[rR][\w]*[fF]|\bmkfs\b|\bdiskutil\s+erase',
    'privileged':r'\bsudo\s+|\bchmod\s+777\b',
    'sensitive_path':r'(?i)(?:\.env(?:\.local)?|id_rsa|seed_phrase|wallet\.dat|bitcoin\.conf)',
    'opaque_decode':r'(?i)(?:base64\s+-[dD]|base64\.b64decode|frombase64string)',
}
DEFAULT_MAX_BYTES=10*1024*1024

def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def read_version(raw):
    m=re.search(r'(?:^|\s)v?(\d+)\.(\d+)\.(\d+)(?:[-+][^\s]+)?',raw.strip())
    return tuple(map(int,m.groups())) if m else None

def cmd_output(args, timeout=5):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
        return {'returncode':p.returncode,'stdout':p.stdout[:2000].strip(),'stderr':p.stderr[:1500].strip()}
    except (OSError,subprocess.TimeoutExpired) as e:return {'returncode':None,'error':str(e)[:400]}

def preflight():
    tools={k:shutil.which(k) for k in ['node','npx','git']}
    node=cmd_output([tools['node'],'--version']) if tools['node'] else None
    parsed=read_version(node.get('stdout','')) if node and node['returncode']==0 else None
    checks={'node_at_least_22_20_0':parsed is not None and parsed>=MIN_NODE,
            'npx_available':tools['npx'] is not None,'git_available':tools['git'] is not None}
    target=pathlib.Path.home()/'.claude/skills/find-skills/SKILL.md'
    return {'timestamp_utc':stamp(),'operation':'preflight','status':'PASS' if all(checks.values()) else 'BLOCKED','checks':checks,'tools':tools,'node_version':node,'install_target':str(target),'existing_target':target.exists(),'target_is_symlink':target.is_symlink(),'recommended_action':'preserve existing files; do not install until source review and authorization'}

def plan():
    p=preflight()
    return {'timestamp_utc':stamp(),'operation':'plan','status':'PASS' if p['status']=='PASS' and not p['existing_target'] else 'BLOCKED',
            'preflight':p,'command':['npx','skills','add','vercel-labs/skills','--skill','find-skills','-g','-a','claude-code','--copy','-y'],
            'environment':{'DISABLE_TELEMETRY':'1'},'execution':'NOT_EXECUTED',
            'steps':['source integrity and static audit','explicit authorization','backup any intended change','no-clobber precondition','execute once in authorized terminal','verify copied SKILL.md and global list','confirm in new Claude Code session'],
            'reason':'existing installation must not be overwritten' if p['existing_target'] else 'preflight/authorization gates required'}

def scan_source(root):
    if not root.is_absolute() or not root.is_dir():
        return {'timestamp_utc':stamp(),'operation':'audit','status':'BLOCKED','reason':'absolute existing source directory required'}
    root=root.resolve(strict=True)
    files=[];findings=[];unsafe=[];total=0
    for dirpath,dirs,names in os.walk(root,followlinks=False):
        d=pathlib.Path(dirpath)
        for dn in list(dirs):
            child=d/dn
            if child.is_symlink():unsafe.append({'path':str(child.relative_to(root)),'reason':'symlink directory not followed'});dirs.remove(dn)
            elif dn in ('.git','node_modules','__pycache__'):dirs.remove(dn)
        for name in sorted(names):
            f=d/name;relative=f.relative_to(root).as_posix()
            if f.is_symlink():unsafe.append({'path':relative,'reason':'symlink not read'});continue
            if not f.is_file():unsafe.append({'path':relative,'reason':'nonregular file'});continue
            size=f.stat().st_size;total+=size
            if size>DEFAULT_MAX_BYTES:unsafe.append({'path':relative,'reason':'file too large'});continue
            data=f.read_bytes();entry={'path':relative,'size':len(data),'sha256':sha(data)}
            files.append(entry)
            if b'\0' in data:unsafe.append({'path':relative,'reason':'binary file requires separate review'});continue
            content=data.decode('utf8',errors='replace')
            if '\ufffd' in content:unsafe.append({'path':relative,'reason':'non-UTF8 text requires review'})
            for rule,pat in RISK_PATTERNS.items():
                for i,line in enumerate(content.splitlines(),1):
                    if re.search(pat,line,re.I):
                        findings.append({'path':relative,'line':i,'rule':rule,'snippet':line.strip()[:160]})
    skill=root/'SKILL.md';valid=skill.is_file() and not skill.is_symlink() and skill.read_text('utf8').startswith('---\n')
    status='PASS' if valid and not findings and not unsafe else ('BLOCKED' if not valid or unsafe else 'UNKNOWN')
    return {'timestamp_utc':stamp(),'operation':'audit','status':status,'source':str(root),'files':files,'total_bytes':total,'findings':findings,'unsafe':unsafe,'skill_frontmatter':valid,
            'semantic_security_clearance':False,'installation_authorized':False}

def verify(path):
    if not path.is_absolute():return {'operation':'verify','status':'BLOCKED','reason':'absolute target path required'}
    if not path.exists() or not path.is_file():return {'operation':'verify','status':'FAIL','path':str(path),'reason':'missing SKILL.md'}
    if path.is_symlink():return {'operation':'verify','status':'BLOCKED','path':str(path),'reason':'copy mode expected regular non-symlink file'}
    content=path.read_bytes();valid=content.startswith(b'---\n') and b'name: find-skills' in content[:2000]
    return {'timestamp_utc':stamp(),'operation':'verify','path':str(path),'status':'PASS' if valid else 'FAIL','sha256':sha(content),'bytes':len(content),'content_valid':valid,'global_cli_listing':'NOT_CHECKED','new_claude_session':'NOT_CHECKED','installation_provenance':'NOT_VERIFIED'}

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('action',choices=['preflight','plan','audit','verify']);p.add_argument('--source');p.add_argument('--path');p.add_argument('--output');a=p.parse_args(argv)
    if a.action=='audit':result=scan_source(pathlib.Path(a.source)) if a.source else {'status':'BLOCKED','reason':'--source required'}
    elif a.action=='verify':result=verify(pathlib.Path(a.path)) if a.path else {'status':'BLOCKED','reason':'--path required'}
    else:result=preflight() if a.action=='preflight' else plan()
    output=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if a.output:
        out=pathlib.Path(a.output)
        if not out.is_absolute():p.error('--output must be an absolute path')
        if out.exists():p.error('--output already exists (no overwrite)')
        out.parent.mkdir(parents=True,exist_ok=True)
        with out.open('x',encoding='utf8') as f:f.write(output)
    print(output,end='')
    return 0 if result['status']=='PASS' else 3
if __name__=='__main__':sys.exit(main())
