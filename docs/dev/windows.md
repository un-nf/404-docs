---
title: Windows
description: Run 404 on Windows through the WSL2 distro bundle, populate the runtime contract it expects, trust the generated CA on the host, and route browser traffic through the local listener.
---

# Windows

This is the Windows self-hosted path.

It uses the WSL2 distro bundle. This page does not document running the raw Windows STATIC binary as the normal Windows operator path.

---

## Before you start

- WSL2 must be available on the machine
- the current public profile catalog is `chrome-windows`, `edge-windows`, and `firefox-windows`
- choose the profile that matches your real browser family before you write the runtime config
- the runtime listens on `127.0.0.1:4040` on the Windows side once the distro is running
- the local control plane uses port `4042`

For the exact tagged release page, use [{{ latest_github_release_tag }}]({{ latest_github_release_url }}).

---

## 1. Download the distro bundle

If you want the stable operator path, fetch the signed manifest first and then the tarball it names:

```powershell
$base = "https://updates.404privacy.com"
$manifestPath = Join-Path $HOME "Downloads\404-distro-manifest.json"
$archivePath = Join-Path $HOME "Downloads\404-distro.tar.gz"

Invoke-WebRequest "$base/distro/manifest.json" -OutFile $manifestPath
$manifest = Get-Content $manifestPath | ConvertFrom-Json
Invoke-WebRequest "$base$($manifest.artifact_path)" -OutFile $archivePath
```

If you prefer GitHub-hosted release assets, download `404-distro.tar.gz` from [{{ latest_github_release_tag }}]({{ latest_github_release_url }}).

---

## 2. Stage profiles, control token, and runtime config

The distro boot contract expects all runtime state on the Windows side. Create those directories first:

```powershell
$profile = "edge-windows"
$roamingRoot = Join-Path $env:APPDATA "404\static"
$profilesDir = Join-Path $roamingRoot "profiles"
$runtimeToml = Join-Path $roamingRoot "static.runtime.toml"
$wslRoot = Join-Path $env:LOCALAPPDATA "404\wsl"
$controlToken = Join-Path $wslRoot "control-token"

New-Item -ItemType Directory -Force -Path $profilesDir | Out-Null
New-Item -ItemType Directory -Force -Path $wslRoot | Out-Null
Set-Content -Path $controlToken -Value ([guid]::NewGuid().ToString("N")) -NoNewline
```

The release assets do not bundle the `profiles/` directory. Pull the current catalog from the runtime repository and copy it into the Windows runtime path:

```powershell
$repoRoot = Join-Path $env:USERPROFILE "Desktop\404-runtime"
git clone --depth 1 https://github.com/un-nf/404.git $repoRoot
Copy-Item -Recurse -Force "$repoRoot\src\STATIC_proxy\profiles\*" $profilesDir
```

Write the runtime config the distro expects. Change `$profile` if you want `chrome-windows` or `firefox-windows` instead:

```powershell
@"
[listener]
bind_address = "0.0.0.0"
bind_port = 4040
proxy_protocol = "tls"

[control]
bind_address = "0.0.0.0"
token_path = "/mnt/c/Users/$env:USERNAME/AppData/Local/404/wsl/control-token"

[tls]
keystore = { mode = "file", service = "404.static_proxy", account = "ca_key" }

[pipeline]
profiles_path = "/mnt/c/Users/$env:USERNAME/AppData/Roaming/404/static/profiles"
default_profile = "$profile"
js_debug = false
alt_svc_strategy = "normalize"

[http3]
enabled = false
bind_address = "0.0.0.0"
bind_port = 4041

[telemetry]
mode = "stdout"
"@ | Set-Content -Path $runtimeToml
```

---

## 3. Import the distro and write the Windows username file

Import the tarball into WSL2:

```powershell
$archivePath = Join-Path $HOME "Downloads\404-distro.tar.gz"
$installRoot = Join-Path $env:LOCALAPPDATA "404\wsl\distribution"

wsl --import 404 $installRoot $archivePath --version 2
```

Then write the username file the distro boot script reads:

```powershell
wsl -d 404 -- sh -lc 'printf "%s\n" "$0" > /opt/404/win-user' $env:USERNAME
```

---

## 4. Start the runtime

Launch the distro:

```powershell
wsl -d 404
```

After the distro boots, `404-init.sh` reads `static.runtime.toml`, best-effort attaches `ttl_editor.o` to `eth0`, and starts STATIC in proxy mode.

If you want a quick health check from inside the distro:

```powershell
wsl -d 404 -- sh -lc 'TOKEN=$(cat /mnt/c/Users/'"$env:USERNAME"'/AppData/Local/404/wsl/control-token); wget -qO- --header="X-404-Control-Token: $TOKEN" http://127.0.0.1:4042/status'
```

---

## 5. Trust the generated CA on Windows

Copy the generated CA certificate out of WSL and onto the Windows side:

```powershell
wsl -d 404 -- sh -lc 'cp "$(find /root/.local/share -name static-ca.crt -print -quit)" "/mnt/c/Users/'"$env:USERNAME"'/AppData/Local/404/wsl/static-ca.crt"'
```

Trust it in the Windows root store:

```powershell
certutil.exe -addstore root "$env:LOCALAPPDATA\404\wsl\static-ca.crt"
```

If you use Firefox, also import the same certificate in Firefox:

- Settings -> Privacy & Security -> Certificates -> View Certificates
- Authorities -> Import
- select `%LOCALAPPDATA%\404\wsl\static-ca.crt`
- enable `Trust this CA to identify websites`

---

## 6. Route browser traffic through the listener

The runtime listener is `127.0.0.1:4040` on the Windows side.

For Chrome or Edge:

- Windows Settings -> Network & internet -> Proxy
- enable Manual proxy setup
- Address: `127.0.0.1`
- Port: `4040`

For Firefox:

- Settings -> Network Settings -> Manual proxy configuration
- HTTP Proxy: `127.0.0.1`
- Port: `4040`
- enable `Also use this proxy for HTTPS`

At that point, browser traffic routed through the configured proxy listener will flow through the distro runtime.