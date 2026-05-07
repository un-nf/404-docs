---
title: Product and Repository Model
description: Understand the division between the proprietary 404 desktop application, the open source CLI application, and the account and update infrastructure behind the product.
hide:
  - toc
---

# Product and Repository Model

404 is no longer one thing.

It is one product experience built across three layers:

1. the **desktop app** users install
2. the **runtime stack** that actually mutates traffic
3. the **account and release infrastructure** that distributes builds and validates access

That division should be clear because the licensing and operating model are different at each layer.

---

## The short version

!!! info "Two paths, one documentation site"

    This site covers both:

    - the **proprietary desktop app** distributed through 404privacy.com
    - the **open source runtime stack** you can self-host, inspect, build, and modify yourself

The desktop app is the managed product path.

The CLI application is the repository and operator path.

---

## Layer 1: Desktop app

The desktop app is the product-facing shell.

It owns:

- the React and Tauri user interface
- account and session flow
- desktop update behavior
- host proxy configuration
- host certificate trust workflow
- uninstall cleanup
- runtime orchestration

On Windows, the desktop app now provisions and operates a managed WSL2 Linux runtime by default.

On macOS and some development paths, it still runs against the native runtime backend.

This layer is proprietary. Its current public legal surface lives at:

- [Privacy Policy](https://404privacy.com/privacy/){target="_blank"}
- [Terms of Service](https://404privacy.com/terms/){target="_blank"}
- [EULA](https://404privacy.com/eula/){target="_blank"}

---

## Layer 2: Open source runtime

The runtime stack remains the open source core.

That includes:

- **STATIC**, the local TLS-terminating proxy
- the **WSL distro packaging path** used on Windows
- the **eBPF layer** used for packet-level mutation on Linux

This is the part of 404 that is source-available, auditable, and documented as an operator manual.

If you do not want the managed desktop product path, you can still:

- build STATIC from source
- run the standalone binary directly
- package the WSL distro manually
- attach the eBPF classifier on Linux yourself

That is why this site still contains a full self-hosted manual alongside the desktop app guide.

---

## Layer 3: Account and release infrastructure

The public product path also has an infrastructure layer behind it.

That includes:

- desktop authentication routes
- billing portal access
- signed desktop updater metadata delivery
- signed WSL distro manifest and tarball delivery

Operationally, that layer is what turns a local runtime into a product that can ship managed builds and paid access.

Architecturally, it does **not** change the local-first runtime model. The proxy still runs on the user's machine. The infrastructure exists to distribute binaries, manage access, and publish update metadata.

---

## Why this documentation is split

The split is here to answer two different questions cleanly.

### If you are a user evaluating or running the desktop app

You care about:

- how to install it
- how first run works
- what Windows does with WSL2
- how trust and proxy routing work
- what account and subscription terms apply

### If you are an operator, developer, or auditor

You care about:

- how to build STATIC
- how profiles work
- how the control API works
- how the WSL distro is packaged
- how the eBPF module is built and attached

This site now keeps those two tracks separate instead of pretending they are the same workflow.

---

## Repository map

At a high level:

- the desktop app lives in the `404-APP` repository
- the open source runtime, STATIC, distro path, and eBPF module live in the `404` runtime repository
- the account and public update infrastructure lives in `404-workers`

If you want the product path, start in [Desktop](../getStart/appStart.md).

If you want the CLI path, start in [Self-Hosted/CLI](../dev/index.md).