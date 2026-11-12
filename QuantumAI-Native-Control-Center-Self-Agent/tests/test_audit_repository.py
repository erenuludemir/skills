import os,sys,subprocess,tempfile,pathlib,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
import audit_repository

class AuditRepoTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=pathlib.Path(self.tmp.name)
        self.repo=self.root/'repo'
        self.repo.mkdir()
        for args in [('init','-q'),('config','user.email','test@example.invalid'),('config','user.name','Test')]:
            subprocess.run(['git','-C',str(self.repo),*args],check=True,capture_output=True)
        (self.repo/'skills'/'demo').mkdir(parents=True)
        (self.repo/'skills'/'demo'/'SKILL.md').write_text('---\nname: demo\ndescription: Demo skill.\n---\n',encoding='utf-8')
        (self.repo/'skills'/'demo'/'skill.oms.sig').write_bytes(b'signature-file-present-not-verified')
        subprocess.run(['git','-C',str(self.repo),'add','.'],check=True,capture_output=True)
        subprocess.run(['git','-C',str(self.repo),'commit','-qm','fixture'],check=True,capture_output=True)
    def tearDown(self):
        self.tmp.cleanup()
    def test_file_coverage_and_signature_filename(self):
        result=audit_repository.audit(str(self.repo))
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['tracked_files'],2)
        self.assertEqual(result['root_skills'],1)
        self.assertEqual(result['root_signature_filenames'],1)
        self.assertEqual(result['signature_cryptographic_validation'],'NOT_PERFORMED')
    def test_missing_file_detected(self):
        (self.repo/'skills'/'demo'/'SKILL.md').unlink()
        result=audit_repository.audit(str(self.repo))
        self.assertEqual(result['status'],'FAIL')
        self.assertEqual(len(result['read_errors']),1)
    def test_relative_path_blocked(self):
        self.assertEqual(audit_repository.audit('repo')['status'],'BLOCKED')
    def test_signature_file_missing_detected(self):
        (self.repo/'skills'/'demo'/'skill.oms.sig').unlink()
        result=audit_repository.audit(str(self.repo))
        self.assertEqual(result['status'],'FAIL')
    def test_symlink_target_not_followed(self):
        link=self.repo/'external-link'
        link.symlink_to('/this/should/not/be/read')
        subprocess.run(['git','-C',str(self.repo),'add','external-link'],check=True,capture_output=True)
        result=audit_repository.audit(str(self.repo))
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['tracked_files'],3)
