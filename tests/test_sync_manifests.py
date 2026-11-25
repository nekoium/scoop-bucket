import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

spec = importlib.util.spec_from_file_location(
    "sync_manifests", Path(__file__).resolve().parents[1] / "tools/sync-manifests.py"
)
sync_manifests = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_manifests)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.addCleanup(self.temporary.cleanup)
        self.bucket = Path(self.temporary.name) / "bucket"
        self.assets = {}
        self.manifests = {}
        for app, source in sync_manifests.SOURCES.items():
            release = f"https://example.test/{app}.zip"
            asset = f"{app} release".encode()
            manifest = {
                "version": "1.0.0",
                "architecture": {"64bit": {
                    "url": release,
                    "hash": hashlib.sha256(asset).hexdigest(),
                }},
            }
            self.manifests[app] = json.dumps(manifest).encode()
            self.assets[source] = self.manifests[app]
            self.assets[release] = asset

    def download(self, url):
        value = self.assets[url]
        if isinstance(value, Exception):
            raise value
        return io.BytesIO(value)

    def test_publishes_verified_manifests_and_skips_unchanged_assets(self):
        with patch.object(sync_manifests, "download", side_effect=self.download) as download:
            sync_manifests.sync(self.bucket)
            for app, content in self.manifests.items():
                self.assertEqual((self.bucket / f"{app}.json").read_bytes(), content)
            download.reset_mock()
            sync_manifests.sync(self.bucket)
            self.assertEqual(download.call_count, len(sync_manifests.SOURCES))

    def test_bad_second_release_preserves_both_existing_manifests(self):
        self.bucket.mkdir()
        for app in self.manifests:
            (self.bucket / f"{app}.json").write_text('{"version": "0.1.0"}')
        self.assets["https://example.test/lunaria.zip"] = b"wrong release"
        with patch.object(sync_manifests, "download", side_effect=self.download):
            with self.assertRaisesRegex(ValueError, "lunaria.*SHA-256 mismatch"):
                sync_manifests.sync(self.bucket)
        for app in self.manifests:
            self.assertEqual(json.loads((self.bucket / f"{app}.json").read_bytes()), {"version": "0.1.0"})

    def test_missing_release_does_not_publish_either_manifest(self):
        url = "https://example.test/lunaria.zip"
        self.assets[url] = HTTPError(url, 404, "Not Found", {}, None)
        with patch.object(sync_manifests, "download", side_effect=self.download):
            with self.assertRaises(HTTPError):
                sync_manifests.sync(self.bucket)
        self.assertFalse(self.bucket.exists())


if __name__ == "__main__":
    unittest.main()
