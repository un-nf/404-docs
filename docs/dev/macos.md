---
title: macOS
description: Run the published STATIC binary directly on macOS, stage the profile catalog it expects, trust the generated CA, and route your browser through the local listener.
---

# macOS

This is the direct STATIC path for macOS.

The recommended release assets are packaged operator bundles. Each zip includes the binary, the release manifest files, and the profile catalog you need to start the runtime directly on macOS.

[Download for macOS Apple Silicon](https://github.com/un-nf/404/releases/latest/download/404-macos-aarch64.zip){ .md-button .md-button--primary }
[Download for macOS Intel](https://github.com/un-nf/404/releases/latest/download/404-macos-x64.zip){ .md-button }

Each macOS operator bundle includes:

- `404-runtime/static_proxy`
- `404-runtime/config/static.example.toml`
- `404-runtime/static_proxy-release-manifest.json`
- `404-runtime/static_proxy-release-manifest.json.sig`
- `404-runtime/static_proxy-release-manifest.json.pem`
- `404-runtime/profiles/manifest.json`
- `404-runtime/profiles/firefox-windows.json`
- `404-runtime/profiles/chrome-windows.json`
- `404-runtime/profiles/edge-windows.json`

Extract the zip that matches your machine into your home folder, then keep using that same home-folder path in the commands below.

---

## Before you start

- Apple Silicon uses `static_proxy-macos-aarch64`
- Intel uses `static_proxy-macos-x86_64`
- the current public profile catalog is `chrome-windows`, `edge-windows`, and `firefox-windows`
- this walkthrough defaults to `firefox-windows`
- if you use Chrome, swap `firefox-windows` for `chrome-windows`
- if you use Edge, swap `firefox-windows` for `edge-windows`
- the bundled config listens on `127.0.0.1:4040`
- the local control plane uses `127.0.0.1:4042`

For the current release page, use [{{ latest_github_release_tag }}]({{ latest_github_release_url }}).

---

## 1. Verify the binary appears in the release manifest

Run this in Terminal:

```bash
cat "$HOME/404-runtime/static_proxy-release-manifest.json"
```

If you extracted the zip into a different folder, read the manifest from that location instead.

---

## 2. Extract the bundle into your home folder

If you use Finder:

1. double-click the zip file to unpack it
2. drag the extracted `404-runtime` folder into your home folder
3. confirm the final path is `$HOME/404-runtime`

If you want to do it from Terminal, run this:

```bash
ditto -x -k "$HOME/Downloads/404-macos-aarch64.zip" "$HOME"
chmod +x "$HOME/404-runtime/static_proxy"
```

If you are on Intel, replace `404-macos-aarch64.zip` with `404-macos-x64.zip`.

!!! note "Working directory"

	The Terminal commands below assume the bundle lives at `$HOME/404-runtime`.

	Start each session with:

	```bash
	cd "$HOME/404-runtime"
	```

---

## 3. Inspect the profile catalog and start STATIC

List the available profiles:

```bash
cd "$HOME/404-runtime"
./static_proxy --config ./config/static.example.toml --list-profiles
```

Start the runtime with the profile that matches your browser family:

```bash
cd "$HOME/404-runtime"
./static_proxy --config ./config/static.example.toml --profile firefox-windows
```

Use `chrome-windows` for Chrome or `edge-windows` for Edge.

---

## 4. Trust the generated CA

Ask the local control plane where the CA lives:

```bash
curl -s http://127.0.0.1:4042/ca/status
```

Then trust the `static-ca.crt` path it reports:

```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /path/to/static-ca.crt
```

If you use Firefox, import the same certificate in Firefox under Settings -> Privacy & Security -> Certificates -> View Certificates -> Authorities.

---

## 5. Route browser traffic through STATIC

The bundled config listens on `127.0.0.1:4040`.

For Chrome or Edge:

- System Settings -> Network -> your active interface -> Details -> Proxies
- enable the local proxy path that fits your setup and point it at `127.0.0.1:4040`

For Firefox:

- Settings -> Network Settings -> Manual proxy configuration
- HTTP Proxy: `127.0.0.1`
- Port: `4040`
- enable `Also use this proxy for HTTPS`

If you launch STATIC with a custom port, route the browser to that port instead.