"""Copy app-owned manifests after verifying their published release assets."""

import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

SOURCES = {
    "myosotis": "https://raw.githubusercontent.com/nekoium/Myosotis/master/bucket/myosotis.json",
    "lunaria": "https://raw.githubusercontent.com/nekoium/Lunaria/main/bucket/lunaria.json",
}


def download(url):
    request = Request(url, headers={"User-Agent": "nekoium-scoop-bucket"})
    return urlopen(request, timeout=60)


def sync(bucket):
    updates = {}
    for app, source in SOURCES.items():
        with download(source) as response:
            content = response.read()
        manifest = json.loads(content)
        target = bucket / f"{app}.json"
        if target.exists() and json.loads(target.read_bytes()) == manifest:
            continue
        for package in manifest["architecture"].values():
            digest = hashlib.sha256()
            with download(package["url"]) as response:
                for chunk in iter(lambda: response.read(1024 * 1024), b""):
                    digest.update(chunk)
            if digest.hexdigest() != package["hash"].lower():
                raise ValueError(f"{app} {manifest['version']}: release SHA-256 mismatch")
        updates[target] = content

    # Verify every changed release before writing any manifest.
    bucket.mkdir(parents=True, exist_ok=True)
    for target, content in updates.items():
        target.write_bytes(content)
        print(f"Updated {target.name}")
    if not updates:
        print("All manifests are current.")


if __name__ == "__main__":
    sync(Path(__file__).resolve().parent.parent / "bucket")
