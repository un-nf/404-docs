---
title: WSL Distro and Runtime Packaging
description: Download, build, package, publish, import, and manually operate the 404 WSL runtime artifact. Covers the public distro contract, exact CI-aligned build steps, and the boot assumptions you must satisfy if you run it yourself.
hide:
  - toc
---

# WSL Distro and Runtime Packaging

This page is part of the **open source self-hosted/runtime manual**.

It documents the Linux runtime artifact that the Windows desktop app consumes by default, but you can also work with that artifact directly as an operator.

---

## What this artifact is

The current distro path packages an Alpine-based WSL-importable root filesystem that contains:

- the musl STATIC binary
- the compiled `ttl_editor.o` object
- the Linux-side startup entrypoint
- the boot configuration WSL needs to start that runtime

This is not just a side experiment anymore. It is the production runtime path for Windows.

---

## Public release contract

The public update origin exposes:

- `/distro/manifest.json`
- `/distro/manifest.json.sig`
- `/distro/<tag>/404-distro.tar.gz`
- `/distro/<tag>/manifest.json`
- `/distro/<tag>/manifest.json.sig`

The stable manifest points at a versioned immutable tarball path.

The desktop app verifies:

- the manifest signature
- the tarball hash inside the signed manifest

The current release-manifest shape is:

```json
{
  "version": "v1.2.3",
  "sha256": "<hex>",
  "artifact_path": "/distro/v1.2.3/404-distro.tar.gz",
  "published_at": "2026-05-06T00:00:00.000Z"
}
```

---

## Download the published distro

For most users, the desktop app should be the thing that downloads and verifies the distro.

If you want the artifact directly as an operator, treat the public origin as a manifest-first contract.

Typical fetch sequence:

```bash
BASE_URL="https://updates.404privacy.com"

curl -O "$BASE_URL/distro/manifest.json"
curl -O "$BASE_URL/distro/manifest.json.sig"
```

Then read the manifest and fetch the referenced tarball path:

```bash
curl -O "$BASE_URL/distro/v1.2.3/404-distro.tar.gz"
```

!!! warning "What this page does not pretend to solve"

    The public operator walkthrough for independent signature verification should stay aligned with the final public-key distribution story.

    Anything that needs a more formal public-key verification guide belongs in `PLAN.md` until that operator story is frozen cleanly.

---

## Build it locally

The distro build is a CI-backed packaging path now, not a hand-waved future workflow.

The release job currently does this:

1. build the musl STATIC binary for `x86_64-unknown-linux-musl`
2. build `src/ebpf/ttl_editor.o`
3. package `dist/404-distro.tar.gz`
4. generate `dist/distro/manifest.json`
5. sign that manifest
6. publish stable and versioned objects

If you want to mirror the local parts of that path yourself, this is the closest manual sequence.

### 1. Install the musl and Linux build dependencies

On Debian/Ubuntu-like hosts:

```bash
sudo apt-get update
sudo apt-get install -y \
  clang \
  llvm \
  musl-tools \
  pkg-config \
  cmake \
  ninja-build \
  perl \
  make \
  g++ \
  iproute2 \
  libbpf-dev \
  libelf-dev \
  linux-libc-dev
```

### 2. Add the Rust musl target

```bash
rustup target add x86_64-unknown-linux-musl
```

### 3. Build the JS bundle the runtime expects

```bash
npm ci --prefix src/STATIC_proxy/build
```

### 4. Build the musl STATIC binary

```bash
CC_x86_64_unknown_linux_musl=musl-gcc \
CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_LINKER=musl-gcc \
cargo build --release --locked \
  --manifest-path src/STATIC_proxy/Cargo.toml \
  --bin static_proxy \
  --target x86_64-unknown-linux-musl
```

### 5. Build the eBPF object

```bash
make -C src/ebpf clean all
```

### 6. Package the distro tarball

Use the packaging entrypoint:

```sh
./distro/build.sh \
  --static-binary "$PWD/src/STATIC_proxy/target/x86_64-unknown-linux-musl/release/static_proxy" \
  --ttl-object "$PWD/src/ebpf/ttl_editor.o" \
  --version v0.1.0-dev \
  --output "$PWD/dist/404-distro.tar.gz" \
  --image-tag "404-distro-build:local"
```

That script expects two prebuilt inputs:

- a Linux `x86_64-unknown-linux-musl` STATIC binary
- a compiled `ttl_editor.o` object

Output:

- `dist/404-distro.tar.gz`

It stages the rootfs, copies the artifacts into a temporary Docker context, writes `/opt/404/distro-version`, builds a temporary image, then uses `docker create` and `docker export` to emit the final WSL-importable tarball.

---

## Import it manually on Windows

For most users, the desktop app should do this for you.

If you are operating the runtime directly, the lower-level import shape is the normal WSL import pattern:

```powershell
wsl --import 404 C:\path\to\install-root C:\path\to\404-distro.tar.gz --version 2
```

After import, the runtime still expects the desktop-style boot contract.

Current boot behavior inside the distro comes from `/opt/404/404-init.sh`, which does this:

1. reads the Windows username from `/opt/404/win-user`
2. resolves the runtime config at `/mnt/c/Users/<WIN_USER>/AppData/Roaming/404/static/static.runtime.toml`
3. best-effort attaches `ttl_editor.o` to `eth0`
4. starts `/opt/404/static --config <path> --mode proxy`

The interface name in that attach step is currently hard-coded to `eth0` inside `/opt/404/404-init.sh`.

There is no manifest field or runtime TOML field for overriding it yet.

If your WSL network shows up under a different interface name, the manual operator workaround is:

```powershell
wsl -d 404 -- ip link show
wsl -d 404 -- sh -lc 'tc qdisc add dev <interface> clsact 2>/dev/null || true; tc filter add dev <interface> egress bpf da obj /opt/404/ttl_editor.o sec classifier 2>/dev/null || true'
```

So manual operators need to satisfy that contract explicitly.

### Minimum manual setup after import

#### 1. Write the Windows username file inside the distro

```powershell
wsl -d 404 -- sh -lc 'printf "%s\n" "$0" > /opt/404/win-user' $env:USERNAME
```

#### 2. Create the runtime config on the Windows side

Current expected path:

```text
C:\Users\<WIN_USER>\AppData\Roaming\404\static\static.runtime.toml
```

At minimum, that runtime config needs to be internally consistent with the Linux boot path and whatever listener/control contract you want to run.

#### 3. Start the distro

```powershell
wsl -d 404
```

If the boot path is healthy, WSL boot configuration should invoke `/opt/404/404-init.sh` automatically.

---

## What is actually inside the tarball

The current rootfs contract includes:

- `/opt/404/win-user`
- `/opt/404/distro-version`
- `/opt/404/404-init.sh`
- `/opt/404/static`
- `/opt/404/ttl_editor.o`
- `/etc/wsl.conf`
- the Windows-side runtime TOML reachable under `/mnt/c/...`

That is why this artifact is more than "a binary download in a tarball." It is a bootable runtime environment with assumptions.

---

## If you only want to run STATIC

Use the simpler self-hosted path instead:

- [Self-Hosted and CLI](../dev/index.md)
- [Windows](../dev/windows.md)

The distro is the right tool when you want the Linux runtime environment itself, not just the proxy binary.