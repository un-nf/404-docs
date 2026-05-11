---
title: Docker and Build Pipeline
description: How the 404 distribution built on the Rose base is packaged with Docker, the exact local build inputs the rootfs pipeline expects, and how to build, inspect, and export a WSL-importable runtime tarball yourself.
hide:
  - toc
---

# Docker and Build Pipeline

This page documents the **open source** distribution build pipeline.

---

## Packaging

The 404 distribution is built as a minimal Linux root filesystem and exported as a flat root filesystem tarball that Windows can import through WSL.

!!! warning "Use `docker export`, not `docker save`"

    WSL expects an importable root filesystem tarball.

    - `docker export` gives you that.
    - `docker save` gives you an image archive, which is the wrong artifact for `wsl --import`.

---

## Dependencies

- `docker`
- a Linux or Linux-capable build environment for the musl binary and eBPF object
- `src/STATIC_proxy/target/x86_64-unknown-linux-musl/release/static_proxy`
- `src/ebpf/ttl_editor.o`

The STATIC binary must be musl-targeted. A glibc-targeted Linux build is the wrong input for the minimal distribution rootfs.

### Build the runtime bundle dependencies

```bash
npm ci --prefix src/STATIC_proxy/build
```

### Build the musl STATIC binary

```bash
rustup target add x86_64-unknown-linux-musl

CC_x86_64_unknown_linux_musl=musl-gcc \
CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_LINKER=musl-gcc \
cargo build --release --locked \
  --manifest-path src/STATIC_proxy/Cargo.toml \
  --bin static_proxy \
  --target x86_64-unknown-linux-musl
```

### Build the eBPF object

```bash
make -C src/ebpf clean all
```

That Makefile currently checks for:

- `clang`
- `llvm-strip`
- `tc`
- `libbpf` headers
- kernel BPF headers

---

## build.sh

`./distro/build.sh`:

1. Stages the rootfs files
2. Copies the musl STATIC binary into the build context
3. Copies `ttl_editor.o` into the build context
4. Writes `/opt/404/distro-version`
5. Builds the temporary Docker image
6. Creates a container from that image
7. Exports the filesystem and gzips it into `dist/404-distro.tar.gz`

Usage:

```bash
./distro/build.sh \
  --static-binary "$PWD/src/STATIC_proxy/target/x86_64-unknown-linux-musl/release/static_proxy" \
  --ttl-object "$PWD/src/ebpf/ttl_editor.o" \
  --version v0.1.0-dev \
  --output "$PWD/dist/404-distro.tar.gz" \
  --image-tag "404-distro-build:local"
```

---

## Inspect the resulting tarball

After packaging:

```bash
tar -tzf dist/404-distro.tar.gz | head -100
```

Make sure you see the following files:

- `opt/404/static`
- `opt/404/ttl_editor.o`
- `opt/404/404-init.sh`
- `opt/404/distro-version`
- `etc/wsl.conf`

---

## Manual Docker export path

`build.sh` responsibilities:

1. stage `rootfs/` plus the built artifacts into a temporary Docker build context
2. `docker build` that context
3. `docker create` a container from the image
4. `docker export` that container
5. gzip the export stream

!!! note "Expected output"

    The output must be a flat root filesystem tarball, not a Docker image archive.

---

## CI shape

The tagged distro release path automates this process:

1. Builds the musl STATIC binary
2. Build the eBPF object
3. Package the distro tarball
4. Generate the stable manifest
5. Sign the manifest with `DISTRO_MANIFEST_SIGNING_KEY`
6. Publish stable and versioned objects to the public update origin

The tagged release workflow publishes:

- Stable `distro/manifest.json`
- Stable `distro/manifest.json.sig`
- Versioned `distro/<tag>/404-distro.tar.gz`
- Versioned `distro/<tag>/manifest.json`
- Versioned `distro/<tag>/manifest.json.sig`