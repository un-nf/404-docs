---
title: Runtime Repository Map
description: Repository-facing map of the open source runtime, the desktop shell, and the worker-backed release surface that together make up the current 404 delivery model.
hide:
  - toc
---

# Runtime Repository Map

404 maintains multiple repositories that interact with each other.

---

## Open source repository - [404](https://github.com/un-nf/404)

Primary runtime source:

- [GitHub](https://github.com/un-nf/404){target="_blank"}
- [Codeberg](https://codeberg.org/szh/404){target="_blank"}

Contains the following components:

- STATIC
- Profile catalog
- WSL distro packaging path
- eBPF object and build path

---

## Desktop repository - [Proprietary Application](https://404privacy.com/pricing/)

Contains the following components:

- Tauri application
- React UI
- Automated host trust installation
- Automated host proxy configuration
- Automated desktop updates
- Windows WSL distro lifecycle

The desktop repo is the product-facing shell.

---

## Worker repository

The worker-backed service surface exists to deliver:

- Account and licensing routes
- Authenticated download routes
- Desktop updater metadata and payloads
- Public distro manifest and tarball routes

Public runtime-facing routes:

- `/distro/manifest.json`
- `/distro/manifest.json.sig`
- `/distro/<tag>/404-distro.tar.gz`
- `/distro/<tag>/manifest.json`
- `/distro/<tag>/manifest.json.sig`