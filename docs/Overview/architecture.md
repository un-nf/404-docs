---
title: Product and Repository Model
description: Understand the division between the proprietary 404 desktop application, the open source CLI application, and the account and update infrastructure behind the product.
hide:
  - toc
---

# 404 Manages Multiple Repositories

1. [404](https://github.com/un-nf/404) - The open source (AGPLv3_ **stack** ([STATIC](../resources/static.md) Proxy & [Rose](../runtime/distro.md) kernel).
2. 404_APP - The proprietary [**desktop application**](https://404privacy.com/pricing/).
3. 404-workers - The **account, licensure, and release infrastructure** that distributes, builds, and validates access.
4. 404-docs - This documentation page.

---

## TL;DR

!!! info

    This site covers:

    - The **proprietary desktop app** distributed through [404privacy.com](https://404privacy.com)
    - The **open source stack** you can self-host, inspect, build, and modify yourself

---

## [Desktop app](https://404privacy.com/pricing/)

- User Interface (UI)
- Account management
- Easy install
- Automated updates
- Automated proxy configuration
- Automated CA trust certificate trust workflow
- Uninstall & cleanup
- Profile orchestration

!!! Tip "Windows implementation"

    On Windows, the desktop app provisions and operates the 404 distribution, which is built on the Rose base and booted through WSL2 when Linux-side networking features are needed.

Legal documents:

- [Privacy Policy](https://404privacy.com/privacy/){target="_blank"}
- [Terms of Service](https://404privacy.com/terms/){target="_blank"}
- [EULA](https://404privacy.com/eula/){target="_blank"}

---

## [Open source code](https://github.com/un-nf/404)

> Licensed under AGPLv3.

- [**STATIC**](../resources/static.md)
- [**Rose kernel**](../runtime/distro.md)
- [**eBPF module**](../resources/ebpf.md)

---

## Account, licensure, and release infrastructure

- Desktop authentication routes
- Billing portal access
- Signed desktop updater metadata delivery
- Signed distribution manifest and tarball delivery for the Rose-based Linux path

This allows us to ship managed builds and service enterprise users.

!!! success "Local First"

    Software *always* runs locally, or on-prem.

---

If you need help with the 404 application, start here: [Desktop](../getStart/appStart.md).

If you need help with free installation, start here: [Self-Hosted/CLI](../dev/index.md).