import importlib.util, pathlib, subprocess, tempfile, unittest, json, sys
HERE=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('qai_agent',HERE/'scripts/control_center.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestController(unittest.TestCase):
    def test_state_contract(self):
        self.assertEqual(mod.STATE, {'PASS','FAIL','BLOCKED','UNKNOWN'})
    def test_no_repo(self):
        self.assertEqual(mod.repo_metadata(None)['status'],'UNKNOWN')
    def test_relative_repo_is_rejected(self):
        self.assertEqual(mod.repo_metadata('relative/path')['status'],'BLOCKED')
    def test_no_rpc_by_default(self):
        self.assertEqual(mod.bitcoin(None,None)['status'],'UNKNOWN')
    def test_plan_never_auto_applies(self):
        for task in mod.plan({'timestamp_utc':'x','checks':{'service':{'status':'FAIL'}}})['actions']:
            self.assertFalse(task['auto_apply'])
    def test_production_gate_is_blocked(self):
        class Args: repo=None; bitcoin_datadir=None; bitcoin_cli=None
        o=mod.observe(Args())
        self.assertEqual(o['checks']['production_finance']['status'],'BLOCKED')
        self.assertFalse(o['production_ready'])
    def test_cli_modes_and_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            for mode in ('observe','plan','verify','report'):
                p=pathlib.Path(tmp)/(mode+'.json')
                r=subprocess.run([sys.executable,str(HERE/'scripts/control_center.py'),mode,'--output',str(p)],capture_output=True,text=True)
                self.assertEqual(r.returncode,0,r.stderr)
                self.assertEqual(json.loads(p.read_text())['operation'],mode)
    def test_legacy_mode(self):
        r=subprocess.run([sys.executable,str(HERE/'scripts/control_center.py'),'--mode','observe'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
if __name__=='__main__':unittest.main()
