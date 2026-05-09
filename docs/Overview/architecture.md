---
title: Product and Repository Model
description: Understand the division between the proprietary 404 desktop application, the open source CLI application, and the account and update infrastructure behind the product.
hide:
  - toc
---

# Product and Repository Model

Three layers:

1. the **desktop app** users install
2. the **runtime stack** that actually mutates traffic
3. the **account and release infrastructure** that distributes builds and validates access

---

## The short version

!!! info "One documentation site"

    This site covers both:

    - the **proprietary desktop app** distributed through 404privacy.com
    - the **open source runtime stack** you can self-host, inspect, build, and modify yourself

---

## Layer 1: Desktop app

The desktop app:

- User Interface (UI)
- Account management
- Easy install
- Automated updates
- Automated proxy configuration
- Automated CA trust certificate trust workflow
- Uninstall & cleanup
- Profile orchestration

On Windows, the desktop app provisions and operates a managed WSL2 Alpine distribution.

Legal documents:

- [Privacy Policy](https://404privacy.com/privacy/){target="_blank"}
- [Terms of Service](https://404privacy.com/terms/){target="_blank"}
- [EULA](https://404privacy.com/eula/){target="_blank"}

---

## Layer 2: Open source runtime

The runtime stack remains open source.

That includes:

- **STATIC**: localhost TLS-terminating proxy
- the **Rose kernel** for WSL2
- the **eBPF module** used for packet-level mutation.

---

## Layer 3: Account and release infrastructure

The public product path also has an infrastructure layer behind it.

That includes:

- desktop authentication routes
- billing portal access
- signed desktop updater metadata delivery
- signed WSL distro manifest and tarball delivery

This allows us to ship managed builds and service enterprise/power users.

This does **not** change the local-first runtime model. The software still runs locally on the user's machine. 

---

If you need help with the 404 application, start in [Desktop](../getStart/appStart.md).

If you need help with free installation, start in [Self-Hosted/CLI](../dev/index.md).