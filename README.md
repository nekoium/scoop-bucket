# nekoium Scoop bucket

Install [Myosotis](https://github.com/nekoium/Myosotis), a screenshot annotation app, or [Lunaria](https://github.com/nekoium/Lunaria), a desktop vision board, with [Scoop](https://scoop.sh) on Windows x64.

```powershell
scoop bucket add nekoium https://github.com/nekoium/scoop-bucket
scoop install nekoium/myosotis
```

To install Lunaria:

```powershell
scoop install nekoium/lunaria
```

Adding the bucket makes both packages available; it installs only the apps you request. If you already added `nekoium`, run only the install command.

Quit the app before updating:

```powershell
scoop update myosotis
scoop update lunaria
```

Installations using the older `myosotis` and `lunaria` buckets continue to receive the same manifest updates. Existing users do not need to reinstall or change buckets.

Downloads come from each app's GitHub Releases and are verified with SHA-256. Installing or updating downloads files from GitHub. See each project's README for app privacy, requirements, and support.

This bucket is licensed under the [MIT License](LICENSE). Each app retains its own license.
