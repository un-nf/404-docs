---
title: STATIC Proxy
description: Technical reference for the STATIC runtime, including startup rules, config defaults, managed CA storage, launch modes, the request pipeline, the transport boundary, and documented limitations.
hide:
  - toc
---

# STATIC Proxy
> Synthetic Traffic and TLS Identity Camouflage

!!! info "STATIC"
    STATIC is the open source runtime at the center of 404.

---

## Features

- Profile-driven proxy startup
- HTTP proxy and TLS interception behavior
- Shared in-memory profile store
- Localhost control plane
- CA generation and runtime-side custody of the private key
- Injected browser-runtime shaping
- Profile-aware transport planning for upstream fetches

For host trust installation, host proxy settings, account flow, updater UX, or Windows-side import and lifecycle handling for the Rose-based distribution, download the [desktop app](https://404privacy.com/pricing/)

??? abstract "STATIC repository map"

    ```text
    src/STATIC_proxy/
    ├── Cargo.toml                      # Rust crate manifest for STATIC
    ├── assets/
    │   └── js/
    │       ├── behavioral_noise_v1.js  # Runtime-side behavioral noise helper
    │       ├── dist/                   # Built runtime bundle embedded by Rust
    │       └── src/
    │           ├── capabilities/
    │           ├── contexts/
    │           ├── core/
    │           ├── evasion/
    │           ├── identity/
    │           ├── privacy/
    │           ├── spoofing/
    │           └── runtime.js
    ├── build/                         # Node/esbuild workspace for runtime.bundle.js
    │   ├── build.js
    │   └── package.json
    ├── build.rs                       # Rust build hook for embedded assets
    ├── certs/                         # Local development certificates and fixtures
    ├── config/
    │   ├── app.config.toml
    │   ├── static.chrome.toml
    │   └── static.example.toml
    ├── profiles/
    ├── src/
    │   ├── app.rs
    │   ├── assets.rs
    │   ├── behavior/
    │   ├── control.rs
    │   ├── lib.rs
    │   ├── main.rs
    │   ├── telemetry.rs
    │   ├── config/
    │   ├── keystore/
    │   ├── proxy/
    │   ├── tls/
    │   └── utils/
    └── target/                        # Local build output when compiling in place
    ```

---

## Implementation

What STATIC does:

- Shapes the upstream client behavior it controls
- Rewrites request and response state through a deterministic stage pipeline
- Injects a coordinated browser-runtime shaping layer into HTML responses

What STATIC does **not** do:

- Rewrite your host TCP handshake in place
- Guarantee exact packet-perfect parity for every requested TLS persona
- Make cross-engine impersonation coherent
- Replace the separate eBPF layer

---

## Startup

STATIC starts with an explicit profile configuration.

Proxy mode expects one of these:

- `--profile <name>`
- `pipeline.default_profile` in config

If neither exists, proxy mode refuses to start.

---

## Launch

### Sample config path

To use `config/static.example.toml` (or personal config):

```bash
cd src/STATIC_proxy
cargo run -- --config config/static.example.toml --profile edge-windows
```

`config/static.example.toml` defaults:

- listener: `127.0.0.1:4040`
- HTTP/3 placeholder bind: `127.0.0.1:4041`
- control plane: `127.0.0.1:4042`

### Standalone binary path

If no config file is provided, STATIC falls back to built-in CLI defaults and looks for `profiles/` beside the executable.

```bash
./static --list-profiles
./static -- --profile edge-windows
```

Defaults:

- listener: `127.0.0.1:8443`
- HTTP/3 placeholder bind: `127.0.0.1:8444`
- control plane: `127.0.0.1:8445`

??? abstract "static.example.toml"

    ```toml
    [listener]
    bind_address = "127.0.0.1"
    bind_port = 4040
    proxy_protocol = "tls"

    [tls]
    keystore = { mode = "keychain", service = "404.static_proxy", account = "ca_key" }

    [pipeline]
    profiles_path = "../profiles"
    js_debug = false
    alt_svc_strategy = "normalize"
    body_limits = { max_request_body_bytes = 16777216, max_response_body_bytes = 33554432, max_decompressed_html_bytes = 16777216 }

    [http3]
    enabled = false
    bind_address = "127.0.0.1"
    bind_port = 4041

    [telemetry]
    mode = "stdout"
    ```

    Important details:

    - `proxy_protocol = "tls"` is the normal path
    - the control plane is configured separately and binds on `listener.bind_port + 2`
    - body buffering limits are explicit
    - HTTP/3 config exists, but the normal runtime path is HTTP/1.1 and HTTP/2

---

## Managed CA and cache paths

STATIC resolves its managed CA and cache paths under the OS app-data directory.

!!! bug "The legacy TLS path fields exist as compatibility inputs"

Managed paths resolve under the OS-local data directory for the `static_proxy` application name, including:

- `certs/static-ca.crt`
- `certs/static-ca.key.dpapi` on the protected-storage path used by the keystore backend
- `certs/cache`

If you need the exact CA certificate path at runtime, the cleanest user-facing check is the control plane:

```text
GET /ca/status
```

---

## Keystore

The sample config uses:

```toml
keystore = { mode = "keychain", service = "404.static_proxy", account = "ca_key" }
```

That is accurate for the standalone/local path.

For WSL, the runtime TOML authored by the desktop shell switches to file-backed key custody inside the Linux runtime contract.

---

## Modes

STATIC can run in two modes:

- `proxy`
- `control`

`proxy` means full data plane plus control plane.

`control` means control-only sidecar behavior.

The composition root lives in `app.rs`, where STATIC loads the shared `ProfileStore`, constructs the stage pipeline, and starts the control plane with shared readiness and shutdown state.

---

## Shared profiles

One `ProfileStore` is loaded and shared between the:

- Request/response pipeline
- Localhost control plane

That is what makes active-profile reads and selection changes coherent.

---

## Bundled profile model

The profile model is built around browser families first and branded variants second.

Simply:

- Use Chromium-family profiles on Blink-family browsers
- Use Firefox-family profiles on Gecko-family browsers

    
!!! Warning

    STATIC does not stop users from misconfiguring the software. Cross-family spoofing is brittle, so ensure proper configuration.

---

## Request classification and protocol handling

STATIC's inbound routing distinguishes between:

- Direct TLS interception
- HTTP CONNECT proxy traffic
- Plain HTTP proxy traffic

At runtime, the connection path branches into downstream and upstream handling paths, including:

- HTTP/1.1 sessions
- HTTP/2 sessions
- Raw websocket tunneling
- Local runtime asset delivery for `__/static/runtime.js`-style support assets
- Buffered HTML mutation only when response stages actually require it

---

## Deterministic stage pipeline

Stage order:

1. `HeaderProfileStage`
2. `BehavioralNoiseStage`
3. `CspStage`
4. `JsInjectionStage`
5. `AltSvcStage`

This satisfies the following requirements:

- Profile shaping must exist before runtime config is embedded
- CSP handling must happen before the final injected script layout is sent
- Alt-Svc handling happens after the main mutation decisions are made

---

## Transport boundary

STATIC's transport plan is as follows

- Profile data describes the desired upstream transport shape
- STATIC passes that plan into the fetcher/backend boundary
- Actual wire fidelity is bound by what the backend can express

Plan inputs:

- Cipher-suite ordering
- Signature-algorithm ordering
- Supported-group ordering
- ALPN
- Extension ordering
- Delegated credentials
- ALPS settings where applicable
- Session-resumption controls

---

## JS runtime model

The JS runtime boots as a fixed pipeline with a shared registry and entropy state.

Bootstrap order:

1. Runtime registry initialization
2. Native reference capture
3. `Function.prototype.toString` masking
4. CSP nonce capture
5. Config load and validation
6. Entropy initialization
7. Policy initialization
8. Identity, capability, spoofing, evasion, privacy, and iframe modules

---

## Worker and iframe handling

### Workers

Worker and SharedWorker construction is wrapped through bootstrap scripts so STATIC can propagate family and identity state into the worker path.

That is where worker-visible fields such as:

- `navigator.userAgent`
- `platform`
- `languages`
- `hardwareConcurrency`
- Chromium-family `userAgentData` and related branding state

can be shaped coherently.

### Iframes

Iframe propagation is same-origin and selective.

The runtime mirrors selected state into compatible child contexts rather than blindly re-running the entire bootstrap path in every frame.

---

## Limitations

- Exact on-the-wire TLS parity is bounded by the curent transport backend
- Service workers and already-existing worker state remain outside the strongest injected-runtime path
- Users can select incoherent family combinations if they insist on doing that
- STATIC and the eBPF layer are distinct systems even when packaged together