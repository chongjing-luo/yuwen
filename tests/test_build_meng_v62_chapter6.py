import hashlib,json,re,subprocess,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];STAGE=ROOT/"work"/"备课"/"选择性必修下册"/"氓"/"_v62_stage"/"chapter_6";PACKAGE=STAGE/"package";PPTX_DIR=STAGE/"pptx";PPTX=PPTX_DIR/"04_氓_V63第六章课堂课件.pptx"
def run(*a):return subprocess.run(a,cwd=ROOT,text=True,capture_output=True,check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class MengV63Chapter6BuildTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  req=[PACKAGE/"06_氓_V63第六章课程数据快照.json",PACKAGE/"chapter6_package_manifest.json",PPTX,PPTX_DIR/"chapter6_pptx_manifest.json"];missing=[str(x) for x in req if not x.exists()]
  if missing:raise AssertionError("missing: "+", ".join(missing))
 def test_contract(self):
  r=json.loads(run("node","scripts/verify_meng_v62_chapter6.js").stdout);self.assertTrue(r["ok"],r["errors"]);self.assertEqual((6,35),(r["pages"],r["total_minutes"]))
 def test_hashes(self):
  s=json.loads((PACKAGE/"06_氓_V63第六章课程数据快照.json").read_text());self.assertEqual(sha(ROOT/"scripts"/"meng_v62"/"content"/"chapter_6.js"),s["source_sha256"]);m=json.loads((PACKAGE/"chapter6_package_manifest.json").read_text());[self.assertEqual(x["sha256"],sha(PACKAGE/x["name"])) for x in m["files"]]
 def test_progressive_boundaries(self):
  w=(PACKAGE/"06F_氓_V63第六章渐进学习单_C601读后发.md").read_text();first=w.split("请先折到这里",1)[0]
  for x in ["已经离开","清醒决绝","男子心意无常","怨苦无边"]:self.assertNotIn(x,first)
  self.assertIn("□A　□B　□并列",w);self.assertIn("诗没有继续写",w);self.assertIn("六张章末卡",w);self.assertIn("临时便笺",w)
 def test_pptx_notes(self):
  with zipfile.ZipFile(PPTX) as z:
   slides=sorted([n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml",n)],key=lambda n:int(re.search(r"\d+",Path(n).stem).group()));notes=sorted([n for n in z.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml",n)],key=lambda n:int(re.search(r"\d+",Path(n).stem).group()));sx=[z.read(n).decode() for n in slides];nx=[z.read(n).decode() for n in notes]
  self.assertEqual((6,6),(len(sx),len(nx)))
  for pid,x in zip(["C601","C602","C603","C604","C605","C606"],nx):self.assertIn(pid,x);self.assertIn("教师逐字稿",x);self.assertIn("删除本页会失去什么",x)
  visible="\n".join(sx)
  for x in ["已经离开","成功离开","唯一解释","觉醒离开"]:self.assertNotIn(x,visible)
  self.assertIn("两种声音",visible);self.assertIn("忽然写淇与隰",visible);self.assertIn("照见后文",visible)
  self.assertNotIn("反衬的‘没有边’",visible)
  m=json.loads((PPTX_DIR/"chapter6_pptx_manifest.json").read_text());self.assertEqual(6,len(m["physical_slides"]));self.assertEqual(m["sha256"],sha(PPTX))
if __name__=="__main__":unittest.main()
