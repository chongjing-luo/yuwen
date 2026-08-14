import hashlib, json, re, subprocess, unittest, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT/"work"/"备课"/"选择性必修下册"/"氓"/"_v62_stage"/"chapter_2"
PACKAGE=STAGE/"package"; PPTX_DIR=STAGE/"pptx"; PPTX=PPTX_DIR/"04_氓_V62第二章课堂课件.pptx"
def run(*args): return subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True)
def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()
class MengV62Chapter2BuildTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  req=[PACKAGE/"06_氓_V62第二章课程数据快照.json",PACKAGE/"chapter2_package_manifest.json",PPTX,PPTX_DIR/"chapter2_pptx_manifest.json"]
  missing=[str(p) for p in req if not p.exists()]
  if missing: raise AssertionError("build artifacts before read-only tests: "+", ".join(missing))
 def test_contract(self):
  r=json.loads(run("node","scripts/verify_meng_v62_chapter2.js").stdout);self.assertTrue(r["ok"],r["errors"]);self.assertEqual((4,27),(r["pages"],r["total_minutes"]))
 def test_source_sync(self):
  s=json.loads((PACKAGE/"06_氓_V62第二章课程数据快照.json").read_text());self.assertEqual(sha256(ROOT/"scripts"/"meng_v62"/"content"/"chapter_2.js"),s["source_sha256"])
  m=json.loads((PACKAGE/"chapter2_package_manifest.json").read_text())
  for x in m["files"]: self.assertEqual(x["sha256"],sha256(PACKAGE/x["name"]))
 def test_material_order_and_no_answers(self):
  a=(PACKAGE/"03A_氓_V62第二章初读与视线卡_C201读后发.md").read_text();b=(PACKAGE/"03B_氓_V62第二章细读与故事轨道_C202发.md").read_text();self.assertIn("after the complete chapter reading",a);self.assertIn('distribution: "C202 only',b)
  for x in ["女子登上残破的墙","看不见复关，她哭","一定幸福","男子驾车来迎","女子带着嫁妆迁往"]: self.assertNotIn(x,a+b)
 def test_pptx_notes_order_and_frontstage(self):
  with zipfile.ZipFile(PPTX) as z:
   slides=sorted([n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml",n)],key=lambda n:int(re.search(r"\d+",Path(n).stem).group()));notes=sorted([n for n in z.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml",n)],key=lambda n:int(re.search(r"\d+",Path(n).stem).group()));sx=[z.read(n).decode() for n in slides];nx=[z.read(n).decode() for n in notes]
  self.assertEqual((4,4),(len(sx),len(nx)))
  for pid,xml in zip(["C201","C202","C204","C206"],nx): self.assertIn(pid,xml);self.assertIn("教师逐字稿",xml);self.assertIn("删除本页会失去什么",xml)
  self.assertIn("按B键熄暗屏幕",nx[3]);self.assertIn("03A和03B同时翻到背面",nx[3])
  allslides="\n".join(sx)
  for x in ["七词复位","乱序：迁","△待调整","一定幸福","男子驾车来迎","女子带着嫁妆迁往"]: self.assertNotIn(x,allslides)
  for x in ["等待从登高远望开始","读后再发视线卡","车来迎，她带着什么迁嫁"]: self.assertNotIn(x,allslides)
  man=json.loads((PPTX_DIR/"chapter2_pptx_manifest.json").read_text());self.assertEqual(4,len(man["physical_slides"]));self.assertEqual(man["sha256"],sha256(PPTX))
if __name__=="__main__": unittest.main()
