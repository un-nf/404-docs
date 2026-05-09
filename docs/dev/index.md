---
title: Self-Hosted and CLI
description: Choose the open source 404 operator path that matches your platform, then follow the exact runtime, trust, and routing steps for Windows, macOS, Linux, or local source builds.
hide:
  - toc
---

# Self-Hosted and CLI

This section is the open source operator path for 404.

Use it when you want to run the runtime directly, control profiles yourself, work with the WSL distro bundle as infrastructure, or build from source.

Current tagged release: [{{ latest_github_release_tag }}]({{ latest_github_release_url }})

---

## Choose your path

<div class="grid cards" markdown>

-   :material-microsoft-windows:{ .lg .middle } __Windows__

    ---

    Use the Rose kernel via WSL2 bundle.

    [Open the Windows guide](./windows.md){ .md-button .md-button--primary }

-   :material-apple:{ .lg .middle } __macOS__

    ---

    Download and run STATIC directly, trust the generated CA, and point your browser at the local listener.

    [Open the macOS guide](./macos.md){ .md-button .md-button--primary }

-   :material-linux:{ .lg .middle } __Linux__

    ---

    Download and run STATIC directly and, if you need packet-layer mutation, attach the eBPF object manually.

    [Open the Linux guide](./linux.md){ .md-button .md-button--primary }

-   :material-tools:{ .lg .middle } __Developers__

    ---

    Install build dependencies, build STATIC from source, package the WSL distro, and work across all three pathways.

    [Open the developers guide](./developers.md){ .md-button .md-button--primary }

</div>

---

## Helpful tips

- All three paths are local and operator controlled
- The current public profile catalog is `chrome-windows`, `edge-windows`, and `firefox-windows`
- Chromium-family browsers should stay on `chrome-windows` or `edge-windows`
- Firefox should stay on `firefox-windows`
- The proxy generates a local CA and you must trust it before browsers will accept proxied HTTPS
- 404 only affects traffic after you point your browser or operating system at its listener

If you want a managed product experience, use [Desktop](../getStart/appStart.md).