---
title: Runtime Repository Map
description: Repository-facing map of the open source runtime, the desktop shell, and the worker-backed release surface that together make up the current 404 delivery model.
hide:
  - toc
---

# Runtime Repository Map

The documentation split only makes sense if the repository split is also clear.

---

## The open source runtime repository

Primary runtime source:

- [GitHub](https://github.com/un-nf/404){target="_blank"}
- [Codeberg](https://codeberg.org/szh/404){target="_blank"}

This is where the open source runtime lives.

That includes:

- STATIC
- the profile catalog
- the WSL distro packaging path
- the eBPF object and build path

---

## The desktop repository

The desktop shell lives separately.

It owns:

- the Tauri app
- the React UI
- host trust installation
- host proxy state
- desktop updates
- Windows WSL distro lifecycle from the app side

The desktop repo is the product-facing shell over the runtime, not the primary source of truth for STATIC itself.

---

## The worker repository

The worker-backed service surface exists to deliver:

- account and licensing routes
- authenticated download routes
- desktop updater metadata and payloads
- public distro manifest and tarball routes

Public runtime-facing routes now include:

- `/distro/manifest.json`
- `/distro/manifest.json.sig`
- `/distro/<tag>/404-distro.tar.gz`
- `/distro/<tag>/manifest.json`
- `/distro/<tag>/manifest.json.sig`

That matters because the docs can no longer pretend the self-hosted and product release surfaces are unrelated.

---

## Why this page exists

There are now three different kinds of documentation questions:

1. how do I use the product
2. how do I run the runtime myself
3. where does a specific contract actually live

This page is for the third question.