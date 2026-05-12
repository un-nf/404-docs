---
title: Developers
description: Install dependencies and build the open source 404 stack from source for the local macOS or Linux path, the Windows Rose-based distribution path, and the supporting Docker packaging workflow.
---

# Developers

This page is for source builds, packaging work, and local development.

If you only want to download & run published artifacts, go to [Self-Hosted and CLI](./index.md).

---

## Repository layout

- `src/STATIC_proxy/` contains the Rust proxy, local control plane, JS build assets, and the public `profiles/` catalog
- `src/ebpf/` contains the Linux packet-mutation program and its build tooling
- `distro/` contains the packaging path for the 404 distribution built on the Rose base and consumed on Windows

---

## Common dependencies

You need these pieces for most source workflows:

- Rust with the target you plan to build
- Node.js 20 for `src/STATIC_proxy/build`
- a C/C++ toolchain plus `cmake`, `ninja`, `perl`, and `pkg-config`
- `git`

Install the STATIC frontend assets once:

```bash
npm ci --prefix src/STATIC_proxy/build
```

---

## Build STATIC for local macOS or Linux runs

From the repository root:

```bash
cargo build --release --locked --manifest-path src/STATIC_proxy/Cargo.toml --bin static_proxy
```

Then run it against the checked-in profiles directory:

```bash
./src/STATIC_proxy/target/release/static_proxy --profiles-path ./src/STATIC_proxy/profiles --profile edge-windows
```

Swap `edge-windows` for `chrome-windows` or `firefox-windows` if needed.

---

## Build the Windows distribution inputs

The distro packaging path expects two artifacts first:

- a Linux musl STATIC binary
- `src/ebpf/ttl_editor.o`

Install the Linux-side packaging dependencies on a Debian or Ubuntu host:

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
rustup target add x86_64-unknown-linux-musl
```

Build the musl STATIC binary:

```bash
CC_x86_64_unknown_linux_musl=musl-gcc \
CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_LINKER=musl-gcc \
cargo build --release --locked \
  --manifest-path src/STATIC_proxy/Cargo.toml \
  --bin static_proxy \
  --target x86_64-unknown-linux-musl
```

Build the eBPF object:

```bash
make -C src/ebpf clean all
```

---

## Package the distribution tarball

Once those two inputs exist, package the distribution artifact:

```bash
./distro/build.sh \
  --static-binary "$PWD/src/STATIC_proxy/target/x86_64-unknown-linux-musl/release/static_proxy" \
  --ttl-object "$PWD/src/ebpf/ttl_editor.o" \
  --version v0.1.0-dev \
  --output "$PWD/dist/404-distro.tar.gz" \
  --image-tag "404-distro-build:local"
```

That produces a WSL-importable root filesystem tarball for the 404 distribution at `dist/404-distro.tar.gz`.

---

## Use the published guides after you build

- For manual Windows operation of that tarball, use [Windows](./windows.md)
- For direct local binary usage on macOS, use [macOS](./macos.md)
- For direct local binary usage and eBPF attachment on Linux, use [Linux](./linux.md)
- For the packaging contract and publication model, use [Linux for Windows](../runtime/distro.md)