# Maintaining the bucket

The app repositories own their manifests:

- [Myosotis](https://github.com/nekoium/Myosotis/blob/master/bucket/myosotis.json)
- [Lunaria](https://github.com/nekoium/Lunaria/blob/main/bucket/lunaria.json)

Update the app's manifest as part of its release. Keep published release assets immutable. This preserves updates for users of the original app-specific buckets as well as this shared bucket.

The **Sync manifests** workflow runs hourly and can be started manually after a release:

```sh
gh workflow run sync.yml --repo nekoium/scoop-bucket
```

Synchronization verifies the SHA-256 of every changed manifest's release download before copying any manifests. An unavailable asset or incorrect checksum fails the run and leaves the bucket unchanged. GitHub can delay scheduled workflows; start a manual run when publishing a release and confirm it succeeds before announcing Scoop availability.

Do not edit generated files in `bucket/` directly. Update the source manifest instead.

To check or sync locally with Python 3:

```sh
python -m unittest discover -s tests -v
python tools/sync-manifests.py
```

The sync command downloads published release ZIPs for changed manifests. It does not build or launch either app.
