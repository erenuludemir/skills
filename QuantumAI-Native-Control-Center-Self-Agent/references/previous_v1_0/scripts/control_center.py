#!/usr/bin/env python3
"""Safe, read-only local observation; no shell, no network, no mutation."""
import argparse, json, platform, shutil, datetime, pathlib, subprocess

def main():
    p=argparse.ArgumentParser(); p.add_argument('--mode',choices=['observe'],default='observe'); p.add_argument('--output'); a=p.parse_args()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result={'timestamp_utc':now,'mode':'READ_ONLY','host':platform.node(),'platform':platform.platform(),'checks':{},'overall':'UNKNOWN'}
    for tool in ('bitcoin-cli','git','python3','docker','bun'):
        path=shutil.which(tool)
        result['checks'][tool]={'status':'PASS' if path else 'UNKNOWN','executable':path}
    result['checks']['bitcoin_rpc']={'status':'UNKNOWN','reason':'RPC deliberately not called without explicit authorized configuration'}
    result['checks']['financial_production_gate']={'status':'BLOCKED','reason':'No signing, broadcasting or trading permitted'}
    out=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if a.output: pathlib.Path(a.output).write_text(out,encoding='utf-8')
    print(out,end='')
if __name__=='__main__': main()
