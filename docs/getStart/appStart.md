---
title: Desktop Application
description: Install and use the 404 desktop application. Covers getting started, first run behavior, trust and routing, Windows WSL2 runtime behavior, and updates and licensing.
---

# Desktop Application

The desktop application is the managed product path for 404.

It is the fastest way to get from zero to a working local runtime without having to build STATIC, package a distro, or wire system proxy settings by hand.

!!! info "What this page covers"

    This page is for the **desktop application** distributed through 404privacy.com.

    If you want the open source CLI path instead, start here:

    [CLI Application](../dev/index.md){ .md-button }

[Get the desktop app](https://404privacy.com/pricing/){.md-button .md-button--primary target="_blank"}
  [Visit 404privacy.com](https://404privacy.com/){.md-button target="_blank"}

---

  ## Getting Started

  Use the desktop application if you want:

  - a managed installer
  - account-backed access and billing
  - built-in proxy controls
  - managed updates
  - Windows runtime provisioning through WSL2 without working with `wsl.exe` directly

  The shortest path is:

  1. download the current build from 404privacy.com
  2. install the application for your platform
  3. sign in or activate access if your build path requires it
  4. choose your browser family
  5. let the application generate and trust the local CA
  6. start the engine and enable routing when you want traffic to flow through 404

  ---

  ## What the application does

- the user interface
- account and auth flow
- runtime orchestration
- host trust installation
- host proxy routing changes
- desktop updates
- uninstall cleanup

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

## First Run and Daily Use

On first run, the desktop application is doing three things:

- establish local runtime configuration
- establish trust for TLS interception
- make it easy to start or stop the runtime without hand-editing OS settings

The current onboarding flow is built around:

1. choosing your browser family
2. generating and trusting the local CA
3. deciding whether to start the engine with or without system routing changes

For most users, daily use is:

1. open the application
2. confirm trust and runtime status
3. start the engine
4. enable routing when you want traffic to flow through 404
5. disable routing and stop the engine when you are done

Best practice is still simple:

- Chromium-family browsers should use Chromium-family profiles
- Firefox-family browsers should use Firefox-family profiles

---

## Trust, Certificates, and Routing

404 is a TLS-terminating local proxy. That fact drives the entire trust workflow.

The runtime generates a local CA so it can mint leaf certificates for intercepted TLS sessions.

The desktop application then owns the host-side trust workflow around that certificate.

That split matters:

- the runtime owns certificate material generation
- the desktop application owns installing trust into the operating system

Routing is not the same thing as startup.

- Starting the engine brings the runtime up.
- Enabling system routing tells the host OS to send traffic through it.

Those are related, but they are not the same action.

That is why the desktop UI separates engine state from system routing state.

---

## Windows WSL2 Runtime

Windows is the clearest example of the split between the desktop application and the runtime it manages.

The desktop application is the host-facing shell.

The runtime is a Linux environment running inside a managed WSL2 distro named `404`.

On Windows, the normal product path is:

1. fetch a signed distro manifest
2. verify it with the embedded Ed25519 public key
3. download the referenced tarball
4. verify the tarball hash against the signed manifest
5. import or update the `404` WSL distro
6. write the runtime configuration and control token the Linux service expects
7. start the runtime and talk to STATIC through its authenticated control API

The distro contract currently includes:

- `/opt/404/404-init.sh`
- `/opt/404/distro-version`
- `/opt/404/win-user`
- `/opt/404/control-token`
- the packaged `static` runtime binary
- the packaged `ttl_editor.o` object

The Linux runtime does **not** take over host responsibilities that belong to the desktop application.

Windows still owns:

- proxy settings
- trust installation into the OS
- auth and account flow
- desktop updater behavior
- uninstall cleanup

---

## Platform Notes

### Windows

The desktop application defaults to the managed WSL2 runtime described above.

You do **not** need to import the distro manually for the normal product path.

### macOS

The desktop application currently uses the native runtime path rather than WSL2.

It still owns:

- CA trust workflow
- proxy routing changes
- start and stop controls
- update handling

### Linux

The desktop documentation here is primarily written for the supported product install paths exposed publicly today.

If your goal is to run the runtime directly on Linux, the self-hosted manual is the more relevant path.

---

## Updates, Accounts, and Licensing

The desktop application is distributed as a managed product.

That means the product surface includes:

- account-backed access
- billing portal support
- authenticated desktop auth handoff
- managed binary delivery and updates

Read the current product documents at:

- [Privacy Policy](https://404privacy.com/privacy/){target="_blank"}
- [Terms of Service](https://404privacy.com/terms/){target="_blank"}
- [EULA](https://404privacy.com/eula/){target="_blank"}

404 now has two update channels that should be understood separately.

### Desktop application updates

These update the product shell itself.

### Runtime updates on Windows

These update the managed WSL distro the desktop application provisions and controls.

Those paths are related operationally because they share a public origin, but they are not the same thing.

---

## What the application does not change

404 is local-first. The runtime runs on your machine.

The desktop application does **not** turn 404 into a remote proxy network or a hosted browser relay.

It manages a local runtime and local OS integrations around that runtime.