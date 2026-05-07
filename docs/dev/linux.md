---
title: Linux
description: Run the published STATIC binary directly on Linux, stage the profile catalog it expects, trust the generated CA, route browser traffic through the listener, and attach the eBPF object when you need packet-layer mutation.
---

# Linux

This is the direct STATIC path for Linux.

It covers both the proxy runtime and the manual eBPF attach path.

---

## Before you start

- the release asset is `static_proxy-linux-x86_64`
- the current public profile catalog is `chrome-windows`, `edge-windows`, and `firefox-windows`
- the standalone local listener defaults to `127.0.0.1:8443`
- the local control plane defaults to `127.0.0.1:8445`
- packet-layer mutation requires a Linux kernel and the `ttl_editor.o` object from the source tree

For the current release page, use [{{ latest_github_release_tag }}]({{ latest_github_release_url }}).

---

## 1. Stage the binary and profiles

Download `static_proxy-linux-x86_64` from [{{ latest_github_release_tag }}]({{ latest_github_release_url }}), then create a working directory and place the binary there as `static_proxy`:

```bash
mkdir -p "$HOME/404-runtime"
mv "$HOME/Downloads/static_proxy-linux-x86_64" "$HOME/404-runtime/static_proxy"
chmod +x "$HOME/404-runtime/static_proxy"
```

The release assets do not bundle the `profiles/` directory, so clone the repository and copy it in:

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

Use `chrome-windows` for Chromium-family browsers or `firefox-windows` for Firefox.

---

## 3. Trust the generated CA

Ask the local control plane where the CA lives:

```bash
curl -s http://127.0.0.1:8445/ca/status
```

Then trust the `static-ca.crt` path it reports:

```bash
sudo cp /path/to/static-ca.crt /usr/local/share/ca-certificates/static-ca.crt
sudo update-ca-certificates
```

If you use Firefox, import the same certificate into Firefox's Authorities store.

---

## 4. Route browser traffic through STATIC

The default standalone listener is `127.0.0.1:8443`.

For Firefox:

- Settings -> Network Settings -> Manual proxy configuration
- HTTP Proxy: `127.0.0.1`
- Port: `8443`
- enable `Also use this proxy for HTTPS`

For Chromium-family browsers, use your desktop environment's proxy settings and point them at `127.0.0.1:8443`.

If you launch STATIC with a custom port, route the browser to that port instead.

---

## 5. Attach the eBPF object

If you want packet-layer mutation, build and attach the eBPF object from the source tree.

Install the kernel-side build dependencies first:

```bash
sudo apt-get update
sudo apt-get install -y clang llvm libbpf-dev linux-headers-$(uname -r) iproute2
```

Build the object:

```bash
make -C "$HOME/404-source/src/ebpf" clean all
```

Attach it to the egress interface you care about:

```bash
sudo tc qdisc add dev eth0 clsact
sudo tc filter add dev eth0 egress bpf da obj "$HOME/404-source/src/ebpf/ttl_editor.o" sec classifier
```

To remove it later:

```bash
sudo tc filter del dev eth0 egress
sudo tc qdisc del dev eth0 clsact
```

If your interface is not `eth0`, swap in the correct device name.