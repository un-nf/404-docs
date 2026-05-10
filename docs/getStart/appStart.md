---
title: Desktop Application
description: Install and use the 404 desktop application. Covers getting started, first run behavior, trust and routing, Windows WSL2 runtime behavior, and updates and licensing.
---

# Desktop Application

The fastest way to start spoofing your fingerprint without having to manage profiles, updates, or wire system settings by hand.

!!! info "What this page covers"

    This page is for the **desktop application** distributed through [404privacy.com](https://404privacy.com/pricing/).

    If you want the free CLI application instead, start here:

    [CLI Application](../dev/index.md){ .md-button }

[Get the desktop app](https://404privacy.com/pricing/){.md-button .md-button--primary target="_blank"} 
[login](https://404privacy.com/account/){.md-button target="_blank"}

---

## General Information

  Use the desktop application for access to:

  - Automated install
  - Automated updates
  - License-backed access
  - Built-in proxy controls
  - Automatic WSL2 setup on Windows

  The simplest path is:

  1. Download the current build from [404privacy.com](https://404privacy.com/pricing/)
  2. Install the application for your platform
  3. Sign in to activate your license
  4. Let the application generate and trust the local CA
  5. Choose your browser family
  6. Start the application from the dashboard

!!! info

    404 is a TLS-terminating local proxy. The runtime generates a local CA so it can mint leaf certificates for intercepted TLS sessions.

  ---

## Features

- User interface (UI)
- Account and authorization
- Runtime orchestration
- Trust installation
- System configuration
- Updates
- Uninstall & cleanup

On Windows, it also provisions and updates the managed WSL2 distribution that runs STATIC.

---

## Before you install

Read the current legal documents for the product path:

- [Privacy Policy](https://404privacy.com/privacy/){target="_blank"}
- [Terms of Service](https://404privacy.com/terms/){target="_blank"}
- [EULA](https://404privacy.com/eula/){target="_blank"}

Those documents govern the desktop application and account-backed service surface.

They do **not** replace the AGPL terms that govern STATIC itself when you self-host the open source runtime.

---

## Getting started

On first run, the desktop application does three things:

- Configures application
- Configures CA trust
- Configures system settings (proxy, WSL2, routing)

### Setup

1. Choose your browser family
2. Allow application to trust the local CA
3. Start the engine to configure system settings

### Daily use

1. Open the application
2. Confirm trust and runtime status
3. Start the engine
4. Enable routing
5. Disable routing

!!! info "Browser family"

    - Blink-family browsers (Chrome, Edge, Brave, Opera) should use Chromium-family profiles
    - Gecko-family browsers (Firefox, Mullvad, Tor) should use Firefox-family profiles

---

## Platform Notes

### Windows

The desktop application defaults to the managed WSL2 runtime described above.

You do **not** need to import the distro manually for the normal product path.

### WSL2 Runtime

On Windows, the desktop application allows the user to interact with a WSL2 runtime.

The runtime is a Linux kernel running inside a managed distro named `Rose`.

The Windows application does the following:

1. Fetches a signed distro manifest
2. Verifies it with the embedded Ed25519 public key
3. Downloads the referenced tarball
4. Verifies the tarball hash against the signed manifest
5. Imports or updates the `404` WSL distro
6. Writes the runtime configuration and control token the Linux service expects
7. Starts the runtime and talks to STATIC through an authenticated control API

The distro contains:

- The packaged `STATIC` binary
- The packaged eBPF module (`ttl_editor.o`)
- `/opt/404/404-init.sh`
- `/opt/404/distro-version`
- `/opt/404/win-user`
- `/opt/404/control-token`

The Linux runtime does **not** take over host responsibilities that belong to the desktop application.

### macOS

The desktop application uses the native STATIC runtime path rather than WSL2.

### Linux

The desktop documentation here is primarily written for the supported product install paths exposed publicly today.

If your goal is to run the runtime directly on Linux, the self-hosted manual is the more relevant path.