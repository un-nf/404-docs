---
title: macOS
description: Run the published STATIC binary directly on macOS, stage the profile catalog it expects, trust the generated CA, and route your browser through the local listener.
---

# macOS

This is the direct STATIC path for macOS.

The published release assets are raw binaries. They do not bundle the `profiles/` directory, so you need to stage that yourself before you launch the runtime.

---

## Before you start

- Apple Silicon uses `static_proxy-macos-aarch64`
- Intel uses `static_proxy-macos-x86_64`
- the current public profile catalog is `chrome-windows`, `edge-windows`, and `firefox-windows`
- Chromium-family browsers should use `chrome-windows` or `edge-windows`
- Firefox should use `firefox-windows`
- the standalone local listener defaults to `127.0.0.1:8443`
- the local control plane defaults to `127.0.0.1:8445`

For the current release page, use [{{ latest_github_release_tag }}]({{ latest_github_release_url }}).

---

## 1. Stage the binary and profiles

Download the correct macOS release asset from [{{ latest_github_release_tag }}]({{ latest_github_release_url }}), then create a working directory and place the binary there as `static_proxy`:

```bash
mkdir -p "$HOME/404-runtime"
mv "$HOME/Downloads/static_proxy-macos-aarch64" "$HOME/404-runtime/static_proxy"
chmod +x "$HOME/404-runtime/static_proxy"
```

If you are on Intel, rename `static_proxy-macos-x86_64` instead.

The profile catalog currently lives in the source repository. Clone it once and copy the profiles into the runtime directory:

```bash
git clone --depth 1 https://github.com/un-nf/404.git "$HOME/404-source"
cp -R "$HOME/404-source/src/STATIC_proxy/profiles" "$HOME/404-runtime/profiles"
```

---

## 2. Inspect the profile catalog and start STATIC

List the available profiles:

```bash
cd "$HOME/404-runtime"
./static_proxy --profiles-path ./profiles --list-profiles
```

Start the runtime with the profile that matches your browser family:

```bash
cd "$HOME/404-runtime"
./static_proxy --profiles-path ./profiles --profile edge-windows
```

Use `chrome-windows` for Chrome-family browsers or `firefox-windows` for Firefox.

---

## 3. Trust the generated CA

Ask the local control plane where the CA lives:

```bash
curl -s http://127.0.0.1:8445/ca/status
```

Then trust the `static-ca.crt` path it reports:

```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /path/to/static-ca.crt
```

If you use Firefox, import the same certificate in Firefox under Settings -> Privacy & Security -> Certificates -> View Certificates -> Authorities.

---

## 4. Route browser traffic through STATIC

The default standalone listener is `127.0.0.1:8443`.

For Chrome or Edge:

- System Settings -> Network -> your active interface -> Details -> Proxies
- enable the local proxy path that fits your setup and point it at `127.0.0.1:8443`

For Firefox:

- Settings -> Network Settings -> Manual proxy configuration
- HTTP Proxy: `127.0.0.1`
- Port: `8443`
- enable `Also use this proxy for HTTPS`

If you launch STATIC with a custom port, route the browser to that port instead.