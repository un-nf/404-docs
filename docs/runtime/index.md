---
title: Developer Resources
description: Developer-facing documentation for the open source CLI application, the WSL distro artifact, the Docker-based rootfs build pipeline, Linux eBPF integration, and deep reference material.
hide:
  - toc
---

# Developer Resources

This section is the developer-facing documentation for 404.

If you want the product experience, use the Desktop tab. If you want the guided CLI path, use the Self-Hosted/CLI tab.

The developer documentation covers:

- the WSL distro artifact the Windows desktop application consumes
- the Docker packaging path that builds that distro rootfs tarball
- the Linux eBPF layer
- deep reference pages for STATIC, the control plane, profiles, and repository boundaries

---

## Common Links

### [WSL distro packaging and operation](./distro.md)

### [Docker-based distro build steps](./docker.md)

### [Packet-layer mutation details](../resources/ebpf.md)

---

## Current scope

!!! info "The 404 Linux-distro is live"

    The desktop app consumes a signed distro manifest, verifies the referenced tarball, imports the `404` WSL distro, and boots the Linux runtime from there on Windows.

    This documentation contains instructions on setting up a self-hosted version of this.