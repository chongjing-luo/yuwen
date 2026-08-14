import hashlib,json,re,subprocess,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];STAGE=ROOT/"work"/"备课"/"选择性必修下册"/"氓"/"_v62_stage"/"chapter_5";PACKAGE=STAGE/"package";PPTX_DIR=STAGE/"pptx";PPTX=PPTX_DIR/"04_氓_V63第五章课堂课件.pptx"
def run(*args):return subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class MengV63Chapter5BuildTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  req=[PACKAGE/"06_氓_V63第五章课程数据快照.json",PACKAGE/"chapter5_package_manifest.json",PPTX,PPTX_DIR/"chapter5_pptx_manifest.json"];missing=[str(x) for x in req if not x.exists()]
  if missing:raise AssertionError("build artifacts before tests: "+", ".join(missing))
 def test_contract(self):
  r=json.loads(run("node","scripts/verify_meng_v62_chapter5.js").stdout);self.assertTrue(r["ok"],r["errors"]);self.assertEqual((5,31),(r["pages"],r["total_minutes"]))
 def test_hashes(self):
  s=json.loads((PACKAGE/"06_氓_V63第五章课程数据快照.json").read_text());self.assertEqual(sha(ROOT/"scripts"/"meng_v62"/"content"/"chapter_5.js"),s["source_sha256"])
  m=json.loads((PACKAGE/"chapter5_package_manifest.json").read_text());[self.assertEqual(x["sha256"],sha(PACKAGE/x["name"])) for x in m["files"]]
 def test_safe_progression(self):
  w=(PACKAGE/"05E_氓_V63第五章渐进学习单_C501读后发.md").read_text();first=w.split("请先折到这里",1)[0]
  for x in ["系统伪装","所有家人","身体暴力","支持缺失"]:self.assertNotIn(x,first)
  self.assertIn("仍不足以证明什么",w);self.assertIn("第三人称处境句",w)
  self.assertNotIn("三秒沉默里",w);self.assertIn("外面的笑声停下以后",w)
 def test_pptx_notes_and_frontstage(self):
  with zipfile.ZipFile(PPTX) as z:
   slides=sorted([n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml",n)],key=lambda n:int(re.search(r"\d+",Path(n).stem).group()));notes=sorted([n for n in z.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml",n)],key=lambda n:int(re.search(r"\d+",Path(n).stem).group()));sx=[z.read(n).decode() for n in slides];nx=[z.read(n).decode() for n in notes]
  self.assertEqual((5,5),(len(sx),len(nx)))
  for pid,xml in zip(["C501","C502","C503","C504","C505"],nx):self.assertIn(pid,xml);self.assertIn("教师逐字稿",xml);self.assertIn("删除本页会失去什么",xml)
  visible="\n".join(sx)
  for x in ["系统伪装","全家拒绝","身体暴力","受伤者归责"]:self.assertNotIn(x,visible)
  self.assertIn("哪些仍不足以证明",visible);self.assertNotIn("后文照亮细节，不替细节伪造事实",visible);self.assertNotIn("沉默三秒",visible);self.assertIn("沉默三秒","\n".join(nx))
  m=json.loads((PPTX_DIR/"chapter5_pptx_manifest.json").read_text());self.assertEqual(5,len(m["physical_slides"]));self.assertEqual(m["sha256"],sha(PPTX))
if __name__=="__main__":unittest.main()
