import unittest,tempfile,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from account_privacy import update
class PrivacyTests(unittest.TestCase):
 def test_regeneration_is_idempotent_and_covers_root(self):
  with tempfile.TemporaryDirectory(prefix='wootrex-privacy-test-') as directory:
   root=Path(directory);(root/'tools').mkdir()
   shutil.copyfile(ROOT/'tools/account_privacy_content.json',root/'tools/account_privacy_content.json')
   files=['privacy.html']+[l+'/privacy.html' for l in ['cs','en','de','sk','pl']]
   for name in files:
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,p)
   update(root);first={n:(root/n).read_bytes() for n in files};update(root)
   self.assertEqual(first,{n:(root/n).read_bytes() for n in files})
   self.assertEqual((root/'privacy.html').read_text(encoding='utf-8').count('id="account-data-'),2)
if __name__=='__main__':unittest.main()
