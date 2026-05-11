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

## What 404 changes

The desktop app asks for administrator privileges because it changes local trust and routing state.

### CA settings

To intercept TLS locally, STATIC generates a local CA certificate and the desktop app installs trust for that CA into the host OS.

- On Windows, the app installs the `STATIC Local CA` certificate into `LocalMachine\Root`.
- On macOS, the app installs the certificate into the login keychain and then into the System keychain.
- The app keeps local CA material in its managed app data so the runtime can continue minting leaf certificates.

How to reverse it:

- In the app, stop the engine and use the CA removal or cleanup flow if you are resetting the install
- On Windows, remove the `STATIC Local CA` certificate from the machine trust store
- On macOS, remove the `STATIC Local CA` certificate from the login keychain and the System keychain

### Proxy settings

When you enable routing, the app changes your proxy settings to use the local STATIC listener.

- STATIC listens on `127.0.0.1:4040` in the managed runtime config.
- On Windows, the app sets `ProxyEnable`, `ProxyServer`, and `ProxyOverride` under the current user's Internet Settings registry path and also runs `netsh winhttp set proxy`.
- On macOS, the app enables web and secure web proxy settings for each active network service and adds bypass entries for `localhost` and `127.0.0.1`.

How to reverse it:

- In the app, disable routing or run the cleanup/reset flow.
- On Windows, turn the system proxy off and run `netsh winhttp reset proxy`.
- On macOS, disable web and secure web proxy state for the affected network services.

### Windows WSL2 runtime

On **Windows**, the desktop app provisions a custom Linux distribution for TCP/IP fingerprint mutation.

- The released app registers the distro as `404`.
- Downloads a signed distro manifest and tarball, verifies them, imports the distro, and starts it with WSL2.
- Writes host-side WSL state under the app's local data directory in a `wsl/` folder.
- `wsl/` folder includes a `downloads/` cache, a `distribution/` install directory, a `control-token` file, and an `installed-version.json` record.
- App writes runtime files such as `/opt/404/control-token` and `/opt/404/win-user` into the Linux environment.

How to reverse it:

- In the app, stop the engine and use the cleanup/reset flow if you want the managed runtime removed.
- Manually, you can run `wsl --unregister 404` to remove the managed distro.
- After unregistering, remove the app's local `wsl/` state directory if you want the downloaded archive, install directory, and version metadata gone as well.

### Local app-managed files

The app writes normal local application state.

- Config data
- Runtime config
- Downloaded runtime assets
- Managed profiles and profile cache
- Certificates
- Logs

The exact base path depends on your OS, but the app manages its standard config, data, cache, local data, and log directories through the platform's normal application-data locations.

How to reverse it:

- Use the app's cleanup or uninstall/reset flow first so trust and proxy state are removed cleanly
- Remove the app's remaining config, data, cache, local data, and log directories if you want a full wipe

---

## Platform Notes

### Windows

The desktop application defaults to the managed WSL2 runtime described above.

You do **not** need to import the distro manually for the normal product path.

### WSL2 Runtime

On Windows, the desktop application allows the user to interact with a WSL2 runtime.

The runtime is a Linux kernel running inside a managed distro currently registered by the released app as `404`.

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