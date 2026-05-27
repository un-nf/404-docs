---
title: Rose Kernel
description: Download and run the 404 WSL2 distribution directly from GitHub release assets. Includes manual Windows import, runtime contract, and verification commands.
hide:
  - toc
---

# Rose Kernel

This page is part of the **open source self-hosted manual**.

It documents the Linux distribution artifact that runs inside WSL2 on Windows.

---

## What this artifact is

The release artifact is a WSL-importable Linux root filesystem that contains:

- `/opt/404/static` (STATIC binary)
- `/opt/404/ttl_editor.o` (eBPF classifier object)
- `/opt/404/404-init.sh` (startup entrypoint)
- `/etc/wsl.conf` (boot command wiring)
- `/opt/404/distro-version`

You do not need to download STATIC separately when using this distro tarball.

!!! Tip "Available on Windows"

---

## Release assets

GitHub release assets include:

- `404-distro.tar.gz`
- `404-distro-manifest.json`
- `404-distro-manifest.json.sig`
- `404-windows-x64.zip`

`404-windows-x64.zip` is the operator bundle for manual Windows setup. It includes:

- `404-distro.tar.gz`
- distro manifest files
- `AppData/Roaming/404/static/profiles/*`
- `AppData/Roaming/404/static/static.runtime.toml`
- `AppData/Local/404/wsl/control-token`

## Public manifest contract

The public update origin exposes:

- `/distro/manifest.json`
- `/distro/manifest.json.sig`
- `/distro/<tag>/404-distro.tar.gz`
- `/distro/<tag>/manifest.json`
- `/distro/<tag>/manifest.json.sig`

The manifest points at a versioned, immutable tarball path.

Consumers verify:

- Manifest signature
- Tarball hash inside the signed manifest

Release-manifest shape:

```json
{
  "version": "v1.2.3",
  "sha256": "<hex>",
  "artifact_path": "/distro/v1.2.3/404-distro.tar.gz",
  "published_at": "2026-05-06T00:00:00.000Z"
}
```

---

## Download from GitHub release

On Windows, download release assets from the repository Releases page.

For manual setup, download:

- `404-windows-x64.zip`

Optional direct assets:

- `404-distro.tar.gz`
- `404-distro-manifest.json`
- `404-distro-manifest.json.sig`

---

## Manual Windows setup (self-hosted)

### 1. Extract the Windows operator bundle

Example:

```powershell
Expand-Archive -Path .\404-windows-x64.zip -DestinationPath .\404-windows -Force
```

### 2. Copy AppData payload into your Windows profile

From PowerShell:

```powershell
$src = Resolve-Path .\404-windows
robocopy "$src\AppData\Roaming\404" "$env:APPDATA\404" /E
robocopy "$src\AppData\Local\404" "$env:LOCALAPPDATA\404" /E
```

This places:

- `static.runtime.toml` and profiles under `AppData\Roaming\404\static`
- control token under `AppData\Local\404\wsl`

### 3. Import the WSL distro tarball

Choose a distro name. Example uses `rose`:

```powershell
New-Item -ItemType Directory -Force -Path C:\WSL\rose | Out-Null
wsl --import rose C:\WSL\rose .\404-windows\404-distro.tar.gz --version 2
```

You can use any distro name for manual inspection. The desktop app currently manages only the fixed WSL distro name `404`, so use `404` if you expect the Tauri app to control the runtime.

### 4. Write the Windows username expected by distro startup

```powershell
wsl -d rose -- sh -lc "printf '%s\n' '$env:USERNAME' > /opt/404/win-user"
```

Do not use shell positional parameters such as `$0` here. They can write the shell name instead of the Windows username, which makes distro startup look under the wrong `C:\Users\...\AppData` path.

### 5. Start the distro

```powershell
wsl -d rose
```

That opens a shell session and runs the distro boot contract.

---

## What happens on startup

`/opt/404/404-init.sh` does the following:

1. Reads `/opt/404/win-user`
2. Resolves config at `/mnt/c/Users/<WIN_USER>/AppData/Roaming/404/static/static.runtime.toml`
3. Mounts `bpffs` at `/sys/fs/bpf` (best effort)
4. Attaches `ttl_editor.o` to all live `eth*` egress interfaces (best effort)
5. Pins `fingerprint_profiles` at `/sys/fs/bpf/404/fingerprint_profiles`
6. Starts `/opt/404/static --config <path> --mode proxy`

The eBPF attach path is interface-discovery based (`eth*`), and can be overridden with `EGRESS_IFACES`.

---

## Verify runtime state

Check STATIC process:

```powershell
wsl -d rose -- pgrep -a static
```

Check control plane status:

```powershell
curl.exe http://127.0.0.1:4042/status
```

Check pinned eBPF map:

```powershell
wsl -d rose -- bpftool map show pinned /sys/fs/bpf/404/fingerprint_profiles
```

Check attached filters:

```powershell
wsl -d rose -- sh -lc 'for d in $(ip -o link show up | awk -F": " "/: eth[0-9]+:/ {print \$2}"); do echo "== $d =="; tc filter show dev "$d" egress; done'
```

Useful helper scripts from the open-source repo:

- `scripts/verify-distro-publication.sh` verifies that a public origin exposes the stable manifest, signature, and versioned tarball correctly.
- `scripts/build-local-distro.sh` builds the musl STATIC binary, compiles `ttl_editor.o`, and packages a WSL-importable tarball when you need a source-built artifact.

---

## Direct public-origin download flow

If you are fetching from a public origin, use manifest-first retrieval:

```bash
BASE_URL="https://updates.404privacy.com"

curl -O "$BASE_URL/distro/manifest.json"
curl -O "$BASE_URL/distro/manifest.json.sig"
# then fetch the manifest's artifact_path, for example:
curl -O "$BASE_URL/distro/v1.2.3/404-distro.tar.gz"
```

---

## Source-maintainer build path

For source builds of the distro tarball, use the repository build documentation in:

- `404_REL/distro/README.md`
- `404 APP/docs/local-distro-build.md`

The main packaging helper is:

```bash
bash ./scripts/build-local-distro.sh --version v0.0.0-local
```