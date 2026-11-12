#!/usr/bin/env python3
"""Deterministic read-only observability; never mutates services, wallets or repositories."""
import argparse, datetime, hashlib, json, os, pathlib, platform, shutil, subprocess, sys

STATE={'PASS','FAIL','BLOCKED','UNKNOWN'}

def check(cmd, timeout=5, cwd=None):
    try:
        p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=timeout,cwd=cwd,check=False)
        return {'status':'PASS' if p.returncode==0 else 'FAIL','exit_code':p.returncode,'stdout':p.stdout[:1500],'stderr':p.stderr[:350]}
    except (subprocess.TimeoutExpired,OSError) as exc:
        return {'status':'UNKNOWN','reason':type(exc).__name__}

def disk():
    d=shutil.disk_usage(pathlib.Path.home())
    pct=d.used*100/d.total if d.total else 100
    return {'status':'PASS' if pct<95 else 'FAIL','free_bytes':d.free,'used_percent':round(pct,2)}

def repo_metadata(path):
    if path is None:return {'status':'UNKNOWN','reason':'No --repo configured'}
    p=pathlib.Path(path)
    if not p.is_absolute():return {'status':'BLOCKED','reason':'--repo must be an absolute path'}
    if not p.is_dir():return {'status':'FAIL','reason':'Repository path absent'}
    git=shutil.which('git')
    if not git:return {'status':'UNKNOWN','reason':'git missing'}
    top=check([git,'rev-parse','--show-toplevel'],cwd=p)
    if top['status']!='PASS':return top
    sha=check([git,'rev-parse','HEAD'],cwd=p)
    changed=check([git,'status','--porcelain'],cwd=p)
    if sha['status']!='PASS' or changed['status']!='PASS':return {'status':'FAIL','reason':'Git commands failed'}
    return {'status':'PASS','root':top['stdout'].strip(),'commit':sha['stdout'].strip(),'dirty':bool(changed['stdout']),'changed_preview':changed['stdout'][:500]}

def bitcoin(datadir,program):
    if not (datadir and program):return {'status':'UNKNOWN','reason':'RPC not configured; no wallet RPC called'}
    p=pathlib.Path(datadir)
    if not p.is_absolute() or not p.is_dir():return {'status':'BLOCKED','reason':'Bitcoin datadir must be an existing absolute directory'}
    tool=shutil.which(program) if '/' not in program else program
    if not tool or not pathlib.Path(tool).is_file():return {'status':'UNKNOWN','reason':'bitcoin-cli executable unavailable'}
    # Read-only RPC; no wallet commands, no shell, no cookies logged.
    cmd=[tool,'-datadir='+str(p),'getblockchaininfo']
    data=check(cmd,timeout=8)
    if data['status']!='PASS':return {'status':'UNKNOWN','reason':'Read-only RPC unavailable','exit_code':data.get('exit_code')}
    try: info=json.loads(data['stdout'])
    except (ValueError,TypeError):return {'status':'FAIL','reason':'Invalid RPC JSON'}
    wanted=('chain','blocks','headers','initialblockdownload','verificationprogress')
    result={k:info.get(k) for k in wanted}
    ibd=result.get('initialblockdownload')
    result['status']='PASS' if ibd is False and isinstance(result.get('blocks'),int) else 'UNKNOWN'
    return result

def observe(a):
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    checks={'disk':disk(),'repository':repo_metadata(a.repo),'bitcoin_rpc':bitcoin(a.bitcoin_datadir,a.bitcoin_cli),'production_finance':{'status':'BLOCKED','reason':'No live broadcast/signing/transfers'}}
    for tool in ('python3','git','bun','bitcoin-cli','docker'):
        location=shutil.which(tool)
        checks['tool_'+tool]={'status':'PASS' if location else 'UNKNOWN','path':location}
    checks['macos']={'status':'PASS' if sys.platform=='darwin' else 'UNKNOWN','platform':platform.platform()}
    inspected=[k for k in ('disk','repository','bitcoin_rpc') if checks[k]['status'] not in ('UNKNOWN','BLOCKED')]
    overall='FAIL' if any(checks[k]['status']=='FAIL' for k in inspected) else 'PASS' if len(inspected)==3 and all(checks[k]['status']=='PASS' for k in inspected) else 'UNKNOWN'
    return {'timestamp_utc':now,'operation':'observe','execution_mode':'READ_ONLY','overall':overall,'production_ready':False,'checks':checks}

def plan(observed):
    actions=[]
    for name,value in observed['checks'].items():
        if value['status'] in ('FAIL','UNKNOWN'):
            actions.append({'component':name,'current':value['status'],'intent':'investigate','auto_apply':False,'preconditions':['Collect fresh evidence','Review full existing configuration'],'verification':'rerun observe','rollback':'no changes performed'})
    return {'timestamp_utc':observed['timestamp_utc'],'operation':'plan','status':'PASS','mutations_executed':0,'actions':actions,'production_ready':False}

def verify(obs):
    checks={k:v['status'] for k,v in obs['checks'].items()}
    return {'timestamp_utc':obs['timestamp_utc'],'operation':'verify','status':obs['overall'],'checks':checks,'production_gate':'BLOCKED','deployment_status':'UNKNOWN','production_ready':False}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('operation',nargs='?',choices=('observe','plan','verify','report'),default='observe')
    p.add_argument('--mode',choices=('observe',),help='Legacy --mode observe compatibility')
    p.add_argument('--repo');p.add_argument('--bitcoin-datadir');p.add_argument('--bitcoin-cli');p.add_argument('--output')
    a=p.parse_args(argv)
    obs=observe(a)
    if a.operation=='plan':result=plan(obs)
    elif a.operation=='verify':result=verify(obs)
    elif a.operation=='report':result={'operation':'report','observation':obs,'plan':plan(obs),'verification':verify(obs)}
    else:result=obs
    payload=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if a.output:
        dst=pathlib.Path(a.output).expanduser()
        if not dst.is_absolute() or not dst.parent.is_dir():p.error('--output requires an existing absolute parent directory')
        tmp=dst.with_name(dst.name+'.tmp.'+str(os.getpid()))
        with open(tmp,'x',encoding='utf-8') as f:
            os.chmod(tmp,0o600)
            f.write(payload)
        os.replace(tmp,dst)
    print(payload,end='')
    return 0

if __name__=='__main__':sys.exit(main())
