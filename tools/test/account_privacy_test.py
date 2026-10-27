import unittest,tempfile,shutil,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from account_privacy import update
class PrivacyTests(unittest.TestCase):
 def test_regeneration_is_idempotent_and_covers_root(self):
  with tempfile.TemporaryDirectory(prefix='wootrex-privacy-test-') as directory:
   root=Path(directory);(root/'tools').mkdir()
   shutil.copyfile(ROOT/'tools/account_privacy_content.json',root/'tools/account_privacy_content.json')
   files=['privacy.html']+[l+'/'+name for l in ['cs','en','de','sk','pl'] for name in ['privacy.html','delete-account.html']]
   for name in files:
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,p)
   update(root);first={n:(root/n).read_bytes() for n in files};update(root)
   self.assertEqual(first,{n:(root/n).read_bytes() for n in files})
   self.assertEqual((root/'privacy.html').read_text(encoding='utf-8').count('id="account-data-'),2)
 def test_full_generator_preserves_requests_and_sitemap(self):
  with tempfile.TemporaryDirectory(prefix='wootrex-full-web-') as directory:
   root=Path(directory)
   shutil.copytree(ROOT/'tools',root/'tools',ignore=shutil.ignore_patterns('test-runtime','__pycache__','*.pyc'))
   shutil.copytree(ROOT/'assets/fitness',root/'assets/fitness')
   for lang in ['cs','en','de','sk','pl']:
    p=root/lang;p.mkdir();shutil.copyfile(ROOT/lang/'delete-account.html',p/'delete-account.html')
   command=[sys.executable,'-X','utf8',str(root/'tools/build_locales.py')]
   subprocess.run(command,check=True,capture_output=True,encoding='utf-8')
   files=['privacy.html','sitemap.xml']+[l+'/'+n for l in ['cs','en','de','sk','pl'] for n in ['privacy.html','delete-account.html']]
   first={n:(root/n).read_bytes() for n in files}
   subprocess.run(command,check=True,capture_output=True,encoding='utf-8')
   self.assertEqual(first,{n:(root/n).read_bytes() for n in files})
   for lang in ['cs','en','de','sk','pl']:
    self.assertIn('https://wootrex.cz/'+lang+'/delete-account.html',(root/'sitemap.xml').read_text(encoding='utf-8'))
    self.assertIn('id="manual-deletion-request"',(root/lang/'delete-account.html').read_text(encoding='utf-8'))
    policy=(root/lang/'privacy.html').read_text(encoding='utf-8')
    self.assertIn('Supabase Auth',policy)
    self.assertIn('id="feedback-processing-'+lang+'"',policy)
if __name__=='__main__':unittest.main()
