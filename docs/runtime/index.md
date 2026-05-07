---
title: Developer Resources
description: Developer-facing documentation for the open source CLI application, the WSL distro artifact, the Docker-based rootfs build pipeline, Linux eBPF integration, and deep reference material.
hide:
  - toc
---

# Developer Resources

This section is the developer-facing documentation for 404.

If you want the product experience, use the Desktop tab instead. If you want the guided CLI path, use the Self-Hosted/CLI tab instead.

---

## What lives here

The developer documentation covers:

- the WSL distro artifact the Windows desktop application consumes
- the Docker packaging path that builds that distro rootfs tarball
- the Linux eBPF layer
- deep reference pages for STATIC, the control plane, profiles, and repository boundaries

---

## Start here if you need

### CLI installation and walkthrough

Use:

- [Self-Hosted/CLI](../dev/index.md)

### WSL distro packaging and operation

Use:

- [WSL Distro and Runtime Packaging](./distro.md)

### Docker-based distro build steps

Use:

- [Docker and Build Pipeline](./docker.md)

### Packet-layer mutation details

Use:

- [eBPF Guide](../dev/ebpf.md)

---

## Current scope

!!! info "The distro path is live"

    The WSL distro path is not a future note anymore.

    The desktop app already consumes a signed distro manifest, verifies the referenced tarball, imports the `404` WSL distro, and boots the Linux runtime from there on Windows.

That means the developer documentation has to cover more than the standalone CLI binary now.