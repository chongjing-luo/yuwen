from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "meng_v6" / "check_baseline.js"
PATHS = ROOT / "scripts" / "meng_v6" / "paths.js"
LESSON_RELATIVE = Path("work/备课/选择性必修下册/氓")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MengV6BaselineTests(unittest.TestCase):
    def run_checker(self, *args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["node", str(CHECKER), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def build_fixture(self, root: Path) -> tuple[Path, Path]:
        lesson = root / LESSON_RELATIVE
        lesson.mkdir(parents=True)
        artifact = lesson / "06_氓_V5课程数据快照.json"
        artifact.write_text('{"version":"5.3-literary-participation"}\n', encoding="utf-8")
        source_manifest = lesson / "11_氓_V5交付清单_SHA256.txt"
        source_manifest.write_text(
            f"{sha256(artifact)}  {artifact.relative_to(root).as_posix()}\n",
            encoding="utf-8",
        )
        output_manifest = lesson / "_v6_stage" / "baseline_manifest.json"
        return source_manifest, output_manifest

    def test_write_then_verify_records_exact_current_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_manifest, output_manifest = self.build_fixture(root)
            artifact = root / LESSON_RELATIVE / "06_氓_V5课程数据快照.json"
            before_mtime_ns = artifact.stat().st_mtime_ns

            written = self.run_checker(
                "--write-manifest",
                "--project-root",
                str(root),
                "--source-manifest",
                str(source_manifest),
                "--manifest",
                str(output_manifest),
            )
            self.assertEqual(0, written.returncode, written.stderr)

            data = json.loads(output_manifest.read_text(encoding="utf-8"))
            paths = [entry["path"] for entry in data["files"]]
            self.assertEqual(
                sorted(
                    [
                        source_manifest.relative_to(root).as_posix(),
                        (root / LESSON_RELATIVE / "06_氓_V5课程数据快照.json")
                        .relative_to(root)
                        .as_posix(),
                    ]
                ),
                paths,
            )
            self.assertTrue(all(entry["size"] > 0 for entry in data["files"]))
            self.assertTrue(all(len(entry["sha256"]) == 64 for entry in data["files"]))
            self.assertEqual(before_mtime_ns, artifact.stat().st_mtime_ns)

            verified = self.run_checker(
                "--verify",
                "--project-root",
                str(root),
                "--manifest",
                str(output_manifest),
            )
            self.assertEqual(0, verified.returncode, verified.stderr)

    def test_verify_fails_and_names_the_changed_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_manifest, output_manifest = self.build_fixture(root)
            written = self.run_checker(
                "--write-manifest",
                "--project-root",
                str(root),
                "--source-manifest",
                str(source_manifest),
                "--manifest",
                str(output_manifest),
            )
            self.assertEqual(0, written.returncode, written.stderr)

            changed = root / LESSON_RELATIVE / "06_氓_V5课程数据快照.json"
            changed.write_text('{"version":"changed"}\n', encoding="utf-8")
            verified = self.run_checker(
                "--verify",
                "--project-root",
                str(root),
                "--manifest",
                str(output_manifest),
            )

            self.assertNotEqual(0, verified.returncode)
            self.assertIn("06_氓_V5课程数据快照.json", verified.stderr)
            self.assertIn("BASELINE_SHA256_MISMATCH", verified.stderr)

    def test_output_guard_allows_only_v6_stage_and_rejects_v5_names(self):
        stage_output = ROOT / LESSON_RELATIVE / "_v6_stage" / "audit.json"
        v5_output = ROOT / LESSON_RELATIVE / "04_氓_V5课堂课件.pptx"
        disguised_v5 = ROOT / LESSON_RELATIVE / "_v6_stage" / "04_氓_V5课堂课件.pptx"

        script = (
            "const { assertV6OutputPath } = require(process.argv[1]);"
            "try { assertV6OutputPath(process.argv[2]); console.log('allowed'); }"
            "catch (error) { console.error(error.code + ':' + error.message); process.exit(2); }"
        )
        allowed = subprocess.run(
            ["node", "-e", script, str(PATHS), str(stage_output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, allowed.returncode, allowed.stderr)

        for candidate in (v5_output, disguised_v5):
            rejected = subprocess.run(
                ["node", "-e", script, str(PATHS), str(candidate)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, rejected.returncode)
            self.assertIn("V6_OUTPUT_", rejected.stderr)

    def test_output_guard_rejects_a_stage_symlink_that_escapes_the_lesson(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lesson = root / LESSON_RELATIVE
            lesson.mkdir(parents=True)
            escaped = root / "escaped-output"
            escaped.mkdir()
            (lesson / "_v6_stage").symlink_to(escaped, target_is_directory=True)
            candidate = lesson / "_v6_stage" / "audit.json"

            script = (
                "const { assertV6OutputPath } = require(process.argv[1]);"
                "try { assertV6OutputPath(process.argv[2], process.argv[3]); console.log('allowed'); }"
                "catch (error) { console.error(error.code + ':' + error.message); process.exit(2); }"
            )
            rejected = subprocess.run(
                ["node", "-e", script, str(PATHS), str(candidate), str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(0, rejected.returncode)
            self.assertIn("V6_OUTPUT_SYMLINK_ESCAPE", rejected.stderr)

    def test_output_guard_rejects_an_existing_destination_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stage = root / LESSON_RELATIVE / "_v6_stage"
            stage.mkdir(parents=True)
            escaped_file = root / "escaped.json"
            escaped_file.write_text("outside\n", encoding="utf-8")
            candidate = stage / "audit.json"
            candidate.symlink_to(escaped_file)

            script = (
                "const { assertV6OutputPath } = require(process.argv[1]);"
                "try { assertV6OutputPath(process.argv[2], process.argv[3]); console.log('allowed'); }"
                "catch (error) { console.error(error.code + ':' + error.message); process.exit(2); }"
            )
            rejected = subprocess.run(
                ["node", "-e", script, str(PATHS), str(candidate), str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(0, rejected.returncode)
            self.assertIn("V6_OUTPUT_SYMLINK_ESCAPE", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
