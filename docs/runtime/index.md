---
title: Developer Resources
description: Developer-facing documentation for the open source CLI application, the WSL distro artifact, the Docker-based rootfs build pipeline, Linux eBPF integration, and deep reference material.
hide:
  - toc
---

# Developer Resources

> Developer-facing documentation for 404.

If you want the easiest possible experience, use the [404 application](https://404privacy.com/pricing/). If you want the guided CLI path, use the [Self-Hosted/CLI](../dev/index.md) documentation.

This documentation covers:

- WSL distro artifact & Rose kernel
- Docker packaging path
- eBPF layer
- [Reference pages](../resources/index.md) for [STATIC](../resources/static.md), [APIs](../resources/controlPlane.md), [profiles](../resources/profiles.md), and [repository boundaries](../resources/repoDev.md)

---

## Common Links

### [Understanding 404](../resources/repoDev.md)

### [Linux on Windows (WSL)](./distro.md)

### [Docker build](./docker.md)

### [TCP/IP Fingerprint Mutation](../resources/ebpf.md)

---

## Current scope

!!! info "The 404 Linux-distro is live"

    The desktop app consumes a signed distro manifest, verifies the referenced tarball, imports the `404` WSL distro, and boots the Linux runtime from there on Windows.

    This documentation contains instructions on setting up a self-hosted version of this.