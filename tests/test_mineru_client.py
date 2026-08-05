import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import mineru_client


class MinerUTransferTests(unittest.TestCase):
    def test_download_rejects_plain_http_before_starting_transfer(self):
        with mock.patch("subprocess.run") as run:
            with self.assertRaisesRegex(ValueError, "HTTPS"):
                mineru_client.download("http://cdn-mineru.openxlab.org.cn/result.zip", "/tmp/result.zip")

        run.assert_not_called()

    def test_openxlab_download_is_https_only_direct_and_atomic(self):
        url = "https://cdn-mineru.openxlab.org.cn/result.zip?X-Amz-Signature=TOPSECRET"
        captured = {}

        def successful_transfer(args, **kwargs):
            captured["args"] = args
            captured["env"] = kwargs["env"]
            transfer_path = Path(args[args.index("-o") + 1])
            captured["transfer_path"] = transfer_path
            transfer_path.write_bytes(b"mineru-result")
            return subprocess.CompletedProcess(args, 0, "", "")

        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "result.bin"
            with mock.patch.dict(
                os.environ,
                {"HTTPS_PROXY": "http://proxy.invalid:8080", "ALL_PROXY": "socks://proxy.invalid:1080"},
            ):
                with mock.patch("subprocess.run", side_effect=successful_transfer):
                    mineru_client.download(url, str(destination))

            self.assertEqual(destination.read_bytes(), b"mineru-result")
            self.assertNotEqual(captured["transfer_path"], destination)
            self.assertFalse(captured["transfer_path"].exists())

        self.assertIn("--proto", captured["args"])
        self.assertIn("=https", captured["args"])
        self.assertNotIn("HTTPS_PROXY", captured["env"])
        self.assertNotIn("ALL_PROXY", captured["env"])
        self.assertEqual(captured["env"]["NO_PROXY"], "cdn-mineru.openxlab.org.cn")

    def test_failed_download_preserves_existing_file_and_redacts_signed_url(self):
        url = "https://cdn-mineru.openxlab.org.cn/result.zip?X-Amz-Signature=TOPSECRET"

        def failed_transfer(args, **kwargs):
            return subprocess.CompletedProcess(args, 60, "", f"TLS failed for {url}")

        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "result.zip"
            destination.write_bytes(b"previous-good-result")

            with mock.patch("subprocess.run", side_effect=failed_transfer) as run:
                with self.assertRaises(RuntimeError) as raised:
                    mineru_client.download(url, str(destination))

            self.assertEqual(destination.read_bytes(), b"previous-good-result")
            self.assertEqual(list(Path(temp_dir).iterdir()), [destination])

        self.assertEqual(run.call_count, 2)
        self.assertNotIn("TOPSECRET", str(raised.exception))

    def test_invalid_zip_response_does_not_replace_existing_download(self):
        url = "https://cdn-mineru.openxlab.org.cn/result.zip?X-Amz-Signature=TOPSECRET"

        def html_response(args, **kwargs):
            transfer_path = Path(args[args.index("-o") + 1])
            transfer_path.write_bytes(b"<html>temporary gateway response</html>")
            return subprocess.CompletedProcess(args, 0, "", "")

        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "result.zip"
            destination.write_bytes(b"previous-good-result")

            with mock.patch("subprocess.run", side_effect=html_response):
                with self.assertRaisesRegex(RuntimeError, "ZIP"):
                    mineru_client.download(url, str(destination))

            self.assertEqual(destination.read_bytes(), b"previous-good-result")
            self.assertEqual(list(Path(temp_dir).iterdir()), [destination])

    def test_submit_redacts_signed_url_and_uses_hardened_transfer(self):
        upload_url = "https://cdn-mineru.openxlab.org.cn/upload?X-Amz-Signature=TOPSECRET"
        response = {"data": {"batch_id": "batch-1", "file_urls": [upload_url]}}
        captured = {}

        def successful_upload(args, **kwargs):
            captured["args"] = args
            captured["env"] = kwargs["env"]
            return subprocess.CompletedProcess(args, 0, "", "")

        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.pdf"
            source.write_bytes(b"pdf")
            stdout = io.StringIO()
            with mock.patch.object(mineru_client, "_req", return_value=(200, {}, response)):
                with mock.patch("subprocess.run", side_effect=successful_upload):
                    with contextlib.redirect_stdout(stdout):
                        batch_id, _ = mineru_client.submit(
                            [{"path": str(source), "name": "source.pdf"}],
                            extra={"language": "ch"},
                        )

        self.assertEqual(batch_id, "batch-1")
        self.assertNotIn("TOPSECRET", stdout.getvalue())
        self.assertIn("--proto", captured["args"])
        self.assertIn("=https", captured["args"])
        self.assertNotIn("HTTPS_PROXY", captured["env"])

    def test_submit_raises_when_upload_fails(self):
        upload_url = "https://cdn-mineru.openxlab.org.cn/upload?X-Amz-Signature=TOPSECRET"
        response = {"data": {"batch_id": "batch-1", "file_urls": [upload_url]}}

        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.pdf"
            source.write_bytes(b"pdf")
            failed = subprocess.CompletedProcess([], 60, "", f"TLS failed for {upload_url}")
            with mock.patch.object(mineru_client, "_req", return_value=(200, {}, response)):
                with mock.patch("subprocess.run", return_value=failed):
                    with self.assertRaises(RuntimeError) as raised:
                        mineru_client.submit([{"path": str(source), "name": "source.pdf"}])

        self.assertNotIn("TOPSECRET", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
