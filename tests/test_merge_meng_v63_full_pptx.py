import hashlib
import json
import re
import unittest
import zipfile
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
FULL = (
    ROOT
    / "work"
    / "备课"
    / "选择性必修下册"
    / "氓"
    / "_v62_stage"
    / "full"
    / "pptx"
    / "04_氓_V64完整课堂课件_48页逐字稿.pptx"
)
MANIFEST = FULL.with_name("full_v64_pptx_manifest.json")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def numbered(names, pattern):
    matches = [name for name in names if re.fullmatch(pattern, name)]
    return sorted(matches, key=lambda name: int(re.search(r"\d+", Path(name).stem).group()))


class MengV64FullPptxMergeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not FULL.exists() or not MANIFEST.exists():
            raise AssertionError("run scripts/merge_meng_v63_full_pptx.py first")

    def test_manifest_and_hash(self):
        manifest = json.loads(MANIFEST.read_text())
        self.assertEqual(48, manifest["slide_count"])
        self.assertEqual(48, manifest["notes_count"])
        self.assertEqual(manifest["sha256"], sha256(FULL))
        self.assertEqual(48, len(manifest["pages"]))
        self.assertEqual(48, len({page["page_id"] for page in manifest["pages"]}))
        self.assertNotIn("C304", {page["page_id"] for page in manifest["pages"]})
        self.assertIn("S08", {page["page_id"] for page in manifest["pages"]})
        self.assertEqual(
            ["C301", "C302", "C303", "C305", "C306"],
            [page["page_id"] for page in manifest["pages"] if page["module"] == "chapter_3"],
        )
        self.assertEqual(
            ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08"],
            [page["page_id"] for page in manifest["pages"] if page["module"] == "synthesis"],
        )

    def test_slides_notes_and_page_ids_are_bijective(self):
        manifest = json.loads(MANIFEST.read_text())
        with zipfile.ZipFile(FULL) as archive:
            names = archive.namelist()
            slides = numbered(names, r"ppt/slides/slide\d+\.xml")
            notes = numbered(names, r"ppt/notesSlides/notesSlide\d+\.xml")
            slide_rels = numbered(names, r"ppt/slides/_rels/slide\d+\.xml\.rels")
            notes_rels = numbered(names, r"ppt/notesSlides/_rels/notesSlide\d+\.xml\.rels")
            self.assertEqual((48, 48, 48, 48), (len(slides), len(notes), len(slide_rels), len(notes_rels)))
            for index, (page, note_name, slide_rel_name, note_rel_name) in enumerate(
                zip(manifest["pages"], notes, slide_rels, notes_rels), start=1
            ):
                note_xml = archive.read(note_name).decode("utf-8")
                self.assertIn(page["page_id"], note_xml)
                self.assertIn("教师逐字稿", note_xml)
                self.assertIn(f"../notesSlides/notesSlide{index}.xml", archive.read(slide_rel_name).decode())
                self.assertIn(f"../slides/slide{index}.xml", archive.read(note_rel_name).decode())

    def test_presentation_order_has_48_unique_slide_relationships(self):
        ns = {
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
            "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
            "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
        }
        with zipfile.ZipFile(FULL) as archive:
            presentation = etree.fromstring(archive.read("ppt/presentation.xml"))
            relationships = etree.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
        slide_ids = presentation.xpath("p:sldIdLst/p:sldId", namespaces=ns)
        relationship_ids = [slide.get(f"{{{ns['r']}}}id") for slide in slide_ids]
        self.assertEqual(48, len(slide_ids))
        self.assertEqual(48, len(set(relationship_ids)))
        target_by_id = {
            rel.get("Id"): rel.get("Target")
            for rel in relationships.xpath("pr:Relationship", namespaces=ns)
        }
        self.assertEqual(
            [f"slides/slide{index}.xml" for index in range(1, 49)],
            [target_by_id[relationship_id] for relationship_id in relationship_ids],
        )


if __name__ == "__main__":
    unittest.main()
