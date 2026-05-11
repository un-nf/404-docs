---
title: Windows
description: Run 404 on Windows through the 404 distribution booted with WSL2, populate the runtime contract it expects, trust the generated CA on the host, and route browser traffic through the local listener.
---

# Windows

This is the Windows self-hosted path.

It uses the 404 distribution, which is built on the Rose base and booted with WSL2. This page does not document running the raw Windows STATIC binary as the normal Windows operator path.

[Download for Windows x64](https://github.com/un-nf/404/releases/latest/download/404-windows-x64.zip){ .md-button .md-button--primary }

The Windows operator bundle includes:

- `404-distro.tar.gz`
- `404-distro-manifest.json`
- `404-distro-manifest.json.sig`
- `AppData\Roaming\404\static\static.runtime.toml`
- `AppData\Roaming\404\static\profiles\manifest.json`
- `AppData\Roaming\404\static\profiles\firefox-windows.json`
- `AppData\Roaming\404\static\profiles\chrome-windows.json`
- `AppData\Roaming\404\static\profiles\edge-windows.json`
- `AppData\Local\404\wsl\control-token`

Extract `404-windows-x64.zip` directly into your Windows home folder, which is usually `C:\Users\<your-username>`.

That extraction step should place:

- `404-distro.tar.gz`, `404-distro-manifest.json`, and `404-distro-manifest.json.sig` in your home folder
- the full `AppData\Roaming\404\static` tree in the right place
- the `AppData\Local\404\wsl\control-token` file in the right place

---

## Before you start

- WSL2 must be available on the machine because it is the Windows host mechanism used to boot the 404 distribution
- the public profile catalog is `chrome-windows`, `edge-windows`, and `firefox-windows`
- the bundled runtime config defaults to `firefox-windows`
- if you use Chrome, swap `firefox-windows` for `chrome-windows`
- if you use Edge, swap `firefox-windows` for `edge-windows`
- the runtime listens on `127.0.0.1:4040` on the Windows side once the distro is running
- the local control plane uses port `4042`

For the exact tagged release page, use [{{ latest_github_release_tag }}]({{ latest_github_release_url }}).

---

## 1. Verify the download matches the manifest

Run this in PowerShell:

```powershell
$manifest = Get-Content "$HOME\Downloads\404-windows-x64\404-distro-manifest.json" | ConvertFrom-Json
$archiveHash = (Get-FileHash "$HOME\Downloads\404-windows-x64\404-distro.tar.gz" -Algorithm SHA256).Hash.ToLower()

"manifest version: $($manifest.version)"
"manifest artifact path: $($manifest.artifact_path)"
"manifest sha256: $($manifest.sha256)"
"archive sha256:  $archiveHash"
```

The two SHA-256 values should match.

---

## 2. Extract the bundle into your Windows home folder

Right-click `404-windows-x64.zip`, choose `Extract All...`, and set the destination to your Windows home folder.

In the Extract All dialog:

1. click `Browse...`
2. open `This PC → Local Disk (C:) → Users → <your-username>`
3. click `Select Folder`
4. click `Extract`

??? abstract "Powershell command"

    ```powershell
    Expand-Archive -LiteralPath "$HOME\Downloads\404-windows-x64.zip" -DestinationPath "$HOME" -Force
    ```

---

## 3. Change the default profile

!!! info "The default profile is Firefox-Windows"
        
    If you are using a Blink based profile, you'll have to use the `Chrome-Windows` or `Edge-Windows` profile.

- File: `%APPDATA%\404\static\static.runtime.toml`

Line to change:

```toml
default_profile = "firefox-windows"
```

??? abstract "I want to use the Chrome profile"

	Run this in PowerShell:

    ```powershell
    (Get-Content "$env:APPDATA\404\static\static.runtime.toml") -replace 'default_profile = "firefox-windows"', 'default_profile = "chrome-windows"' | Set-Content "$env:APPDATA\404\static\static.runtime.toml"
    ```

??? abstract "I want to use the Edge profile"

	Run this in PowerShell:

    ```powershell
    (Get-Content "$env:APPDATA\404\static\static.runtime.toml") -replace 'default_profile = "firefox-windows"', 'default_profile = "edge-windows"' | Set-Content "$env:APPDATA\404\static\static.runtime.toml"
    ```

This default configuration is as follows:

- Listener on `4040`
- Control plane on `4042`
- File-backed key storage
- Profiles loaded from the local `profiles` directory beside the config file
- control token loaded from the relative Windows local-app-data path

---

## 4. Import the distribution and write the Windows username file

Run these two commands in PowerShell:

```powershell
wsl --import 404 "$env:LOCALAPPDATA\404\wsl\distribution" "$HOME\404-distro.tar.gz" --version 2
wsl -d 404 -- sh -lc 'printf "%s\n" "$0" > /opt/404/win-user' $env:USERNAME
```

---

## 5. Start the runtime and confirm start

Launch the distro:

```powershell
wsl -d 404
```

After the distribution boots, `404-init.sh` reads `static.runtime.toml`, best-effort attaches `ttl_editor.o` to `eth0`, and starts STATIC in proxy mode.

!!! note "About `eth0`"

    The distro init script hard-codes the eBPF attach step to `eth0`.

    There is no separate runtime setting for that interface yet.

    On a normal WSL2 setup, `eth0` is usually the right interface. If your distro uses a different name, the runtime will still start, but the packet-mutation attach step may be skipped.

??? abstract "I need to attach `ttl_editor.o` to a different interface"

    First, list the interfaces inside the distro:

    ```powershell
    wsl -d 404 -- ip link show
    ```

    Then attach the classifier manually, replacing `<interface>` with the correct name:

    ```powershell
    wsl -d 404 -- sh -lc 'tc qdisc add dev <interface> clsact 2>/dev/null || true; tc filter add dev <interface> egress bpf da obj /opt/404/ttl_editor.o sec classifier 2>/dev/null || true'
    ```

    If you want that different interface to persist across boots, you currently have to edit `/opt/404/404-init.sh` inside the distro yourself. The bundled config does not expose an interface selector yet.

Open a second PowerShell window to confirm 404 has started:

```powershell
$token = Get-Content "$env:LOCALAPPDATA\404\wsl\control-token" -Raw
Invoke-RestMethod -Headers @{ "X-404-Control-Token" = $token } http://127.0.0.1:4042/status
```

---

## 6. Trust the generated CA

Fetch the generated CA from the local control plane and write it to disk:

```powershell
$token = Get-Content "$env:LOCALAPPDATA\404\wsl\control-token" -Raw
$ca = Invoke-RestMethod -Headers @{ "X-404-Control-Token" = $token } http://127.0.0.1:4042/ca/status
$ca.cert_pem | Set-Content "$env:LOCALAPPDATA\404\wsl\static-ca.crt"
```

Trust it in the Windows root store:

```powershell
certutil.exe -addstore root "$env:LOCALAPPDATA\404\wsl\static-ca.crt"
```

Manual install:

1. Open `%LOCALAPPDATA%\404\wsl` in File Explorer.
2. Double-click `static-ca.crt`.
3. Click `Install Certificate...`.
4. Select `Current User` and click `Next`.
5. Choose `Place all certificates in the following store` and click `Browse...`.
6. Select `Trusted Root Certification Authorities` and click `OK`.
7. Click `Next` and then `Finish`.

If you use Firefox, you must import the certificate into Firefox:

- Settings → Privacy & Security → Certificates → View Certificates
- Authorities → Import
- select `%LOCALAPPDATA%\404\wsl\static-ca.crt`
- enable `Trust this CA to identify websites`

---

## 7. Route browser traffic through the listener

The runtime listener is located at `127.0.0.1:4040`.

For Chrome or Edge:

- Windows Settings → Network & internet → Proxy
- Enable Manual proxy setup
- Address: `127.0.0.1`
- Port: `4040`

For Firefox:

- Settings → Network Settings → Manual proxy configuration
- HTTP Proxy: `127.0.0.1`
- Port: `4040`
- Check `Also use this proxy for HTTPS`

At that point, browser traffic routed through the configured proxy listener will flow through the distro runtime.