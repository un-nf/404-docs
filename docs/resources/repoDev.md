---
title: Repository Map
description: Map of 404 managed repositories. Including the open source code, the desktop application, and the worker-backed release infrastructure that together make up the 404 ecosystem.
hide:
  - toc
---

# Repository Map

404 maintains multiple repositories that interact with each other.

---

## Open source repository - [404](https://github.com/un-nf/404)

Source repositories:

- [GitHub](https://github.com/un-nf/404){target="_blank"}
- [Codeberg](https://codeberg.org/szh/404){target="_blank"}

Contains the following components:

- STATIC
- Profile catalog
- Rose-based distribution packaging path
- eBPF object and build path

---

## Desktop repository - [Proprietary Application](https://404privacy.com/pricing/)

Contains the following components:

- Tauri application
- React UI
- Automated host trust installation
- Automated host proxy configuration
- Automated desktop updates
- Windows-side lifecycle for the Rose-based distribution booted through WSL2

The desktop repo is the product-facing shell.

---

## Worker repository

The worker-backed service surface exists to deliver:

- Account and licensing routes
- Authenticated download routes
- Desktop updater metadata and payloads
- Public distro manifest and tarball routes

Public distribution-facing routes:

- `/distro/manifest.json`
- `/distro/manifest.json.sig`
- `/distro/<tag>/404-distro.tar.gz`
- `/distro/<tag>/manifest.json`
- `/distro/<tag>/manifest.json.sig`