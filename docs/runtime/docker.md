---
title: Docker and Build Pipeline
description: How the 404 WSL distro is packaged with Docker, the exact local build inputs the rootfs pipeline expects, and how to build, inspect, and export a WSL-importable runtime tarball yourself.
hide:
  - toc
---

# Docker and Build Pipeline

This page documents the **open source** distro build pipeline.

---

## The current packaging model

The WSL runtime is built from an Alpine-based Docker image and exported as a flat root filesystem tarball.

That distinction is important.

!!! warning "Use `docker export`, not `docker save`"

    WSL expects an importable root filesystem tarball.

    - `docker export` gives you that.
    - `docker save` gives you an image archive, which is the wrong artifact for `wsl --import`.

---

## Local prerequisites

You need:

- `docker`
- a Linux or Linux-capable build environment for the musl binary and eBPF object
- `src/STATIC_proxy/target/x86_64-unknown-linux-musl/release/static_proxy`
- `src/ebpf/ttl_editor.o`

The STATIC binary must be musl-targeted. A glibc-targeted Linux build is the wrong input for the Alpine-based rootfs.

---

## Build the required inputs first

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

## What the local build script does

`./distro/build.sh`:

1. stages the rootfs files
2. copies the musl STATIC binary into the build context
3. copies `ttl_editor.o` into the build context
4. writes `/opt/404/distro-version`
5. builds the temporary Docker image
6. creates a container from that image
7. exports the filesystem and gzips it into `dist/404-distro.tar.gz`

Typical invocation:

```bash
./distro/build.sh \
  --static-binary "$PWD/src/STATIC_proxy/target/x86_64-unknown-linux-musl/release/static_proxy" \
  --ttl-object "$PWD/src/ebpf/ttl_editor.o" \
  --version v0.1.0-dev \
  --output "$PWD/dist/404-distro.tar.gz" \
  --image-tag "404-distro-build:local"
```

---

## If you want to inspect the resulting tarball

After packaging:

```bash
tar -tzf dist/404-distro.tar.gz | head -100
```

You should see the runtime files that matter, including:

- `opt/404/static`
- `opt/404/ttl_editor.o`
- `opt/404/404-init.sh`
- `opt/404/distro-version`
- `etc/wsl.conf`

---

## Manual Docker export path

If you want to understand what `build.sh` is abstracting, the manual shape is:

1. stage `rootfs/` plus the built artifacts into a temporary Docker build context
2. `docker build` that context
3. `docker create` a container from the image
4. `docker export` that container
5. gzip the export stream

That is the exact idea the script is wrapping.

The important point is still the same: the output must be a flat root filesystem tarball, not a Docker image archive.

---

## CI shape

The tagged distro release path does the same broad work in automation:

1. build the musl STATIC binary
2. build the eBPF object
3. package the distro tarball
4. generate the stable manifest
5. sign the manifest with `DISTRO_MANIFEST_SIGNING_KEY`
6. publish stable and versioned objects to the public update origin

The tagged release workflow currently publishes:

- stable `distro/manifest.json`
- stable `distro/manifest.json.sig`
- versioned `distro/<tag>/404-distro.tar.gz`
- versioned `distro/<tag>/manifest.json`
- versioned `distro/<tag>/manifest.json.sig`

---

## Why this page exists separately from STATIC build docs

Running STATIC is one workflow.

Packaging the Linux runtime artifact that Windows consumes is a different workflow.

They share code and build inputs, but they solve different problems and deserve separate docs.