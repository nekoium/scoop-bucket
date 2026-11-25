# Distribution validation

The shared bucket was checked with Myosotis 1.0.0 and Lunaria 0.1.0.

## Automated synchronization

The three unit tests cover successful synchronization, unchanged manifests avoiding unnecessary release downloads, incorrect checksums preserving existing manifests, and missing release assets preventing publication. The initial GitHub Actions run passed: [Sync manifests](https://github.com/nekoium/scoop-bucket/actions/runs/45536685828).

The initial sync downloaded both published release ZIPs and verified their SHA-256 against the source manifests. Shared manifests match the app-owned source manifests.

## Scoop package checks

Checks used a temporary Scoop root and cache. Start menu shortcuts were redirected to a temporary folder, and persistent PATH writes were disabled in the validation copy of Scoop. Neither app was launched.

- Both public `nekoium/<app>` install commands downloaded, verified, and extracted the released packages. Executables, command shims, shortcut files, versions, and recorded bucket names were checked.
- Repeating `scoop bucket add nekoium https://github.com/nekoium/scoop-bucket` warned that the bucket existed; the following app installation succeeded.
- Normal update checks reported the latest versions. Forced updates reinstalled both shared-bucket packages successfully.
- Uninstall removed the isolated app folders, command shims, and shortcuts.
- A Myosotis 0.2.1 installation using the original `myosotis` bucket upgraded to 1.0.0 while keeping that bucket as its source.
- Lunaria 0.1.0 installed and completed a forced update through its original `lunaria` bucket. No earlier published Lunaria version was available for a cross-version check.

A validation setup mistake initially allowed Scoop to register the temporary shim folder in the user's PATH. That exact entry was removed and its absence verified before continuing with persistent PATH writes disabled. The user's normal Scoop packages and shortcuts were not modified.

These checks establish package installation and update behavior. They do not qualify app launch, interactive behavior, clipboard handling, global hotkeys, or actual Start menu presentation. Release assets remain unchanged.
