---
title: STATIC Runtime and Data Plane
description: Technical reference for the current STATIC runtime, including startup rules, config defaults, managed CA storage, launch modes, the request pipeline, the transport boundary, and the limits that still matter.
hide:
  - toc
---

# STATIC Runtime and Data Plane

STATIC is the open source runtime at the center of 404.

It is not the desktop app, and it is not the WSL distro by itself. It is the proxy runtime that those higher-level delivery paths wrap, package, and operate.

---

## What STATIC is responsible for

STATIC currently owns:

- profile-driven proxy startup
- HTTP proxy and TLS interception behavior
- the shared in-memory profile store
- the localhost control plane
- CA generation and runtime-side custody of the private key
- injected browser-runtime shaping
- profile-aware transport planning for upstream fetches

If you are looking for host trust installation, host proxy settings, account flow, updater UX, or WSL distro import logic, that belongs somewhere else.

---

## The first important correction

Older writeups sometimes made STATIC sound broader or lower-level than it really is.

What STATIC does **not** do today:

- it does not literally rewrite your host TCP handshake in place
- it does not guarantee exact packet-perfect parity for every requested TLS persona
- it does not make cross-engine impersonation magically coherent just because a profile file asked for it
- it does not replace the separate eBPF layer

What it does do is still substantial:

- it shapes the upstream client behavior it controls
- it rewrites request and response state through a deterministic stage pipeline
- it injects a coordinated browser-runtime shaping layer into HTML responses

---

## Current startup contract

STATIC now starts from an explicit profile decision.

Proxy mode expects one of these:

- `--profile <name>`
- `pipeline.default_profile` in config

If neither exists, proxy mode refuses to start.

That is current behavior, not a recommendation.

---

## Current launch modes

### Sample config path

If `config/static.example.toml` is present and you pass it explicitly, you get the sample-config listener shape:

```bash
cd src/STATIC_proxy
cargo run -- --config config/static.example.toml --profile edge-windows
```

Default listener state in that sample:

- listener: `127.0.0.1:4040`
- HTTP/3 placeholder bind: `127.0.0.1:4041`
- control plane: `127.0.0.1:4042`

### Standalone binary path

If no config file is provided, STATIC falls back to built-in CLI defaults and looks for `profiles/` beside the executable.

```bash
./static --list-profiles
./static -- --profile edge-windows
```

Current built-in defaults in that mode:

- listener: `127.0.0.1:8443`
- HTTP/3 placeholder bind: `127.0.0.1:8444`
- control plane: `127.0.0.1:8445`

That is one of the biggest places older docs drifted.

---

## Current config sample

The repository sample config is:

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
- body buffering limits are now explicit
- HTTP/3 config exists, but the normal runtime path is still HTTP/1.1 and HTTP/2

---

## Managed CA and cache paths

This is another place older docs became misleading.

STATIC now resolves its managed CA and cache paths under the OS app-data directory.

The legacy TLS path fields still exist as compatibility inputs, but they are no longer general-purpose override knobs.

Current managed paths resolve under the OS-local data directory for the `static_proxy` application name, including:

- `certs/static-ca.crt`
- `certs/static-ca.key.dpapi` on the protected-storage path used by the current keystore backend
- `certs/cache`

If you need the exact CA certificate path at runtime, the cleanest operator-facing check is still the control plane:

```text
GET /ca/status
```

---

## Keystore reality

The current sample config uses:

```toml
keystore = { mode = "keychain", service = "404.static_proxy", account = "ca_key" }
```

That is accurate for the standalone/local path.

The desktop-managed WSL path is different. There, the runtime TOML authored by the desktop shell switches to file-backed key custody inside the Linux runtime contract.

So any documentation that implies the runtime is always on a localhost/keychain path is now wrong.

---

## Current modes

STATIC can currently run in two modes:

- `proxy`
- `control`

`proxy` means full data plane plus control plane.

`control` means control-only sidecar behavior.

The composition root lives in `app.rs`, where STATIC loads the shared `ProfileStore`, constructs the stage pipeline, and starts the control plane with shared readiness and shutdown state.

---

## Shared profile state

One `ProfileStore` is loaded and shared between:

- the request/response pipeline
- the localhost control plane

That is what makes active-profile reads and selection changes coherent.

This is also why the docs need to talk about profile state and control routes together rather than as separate side notes.

---

## Current bundled profile model

The shipped runtime path is family-first.

That means the runtime is built around browser families first and branded variants second.

Current operator guidance is simple and still correct:

- use Chromium-family profiles on Chromium-family browsers
- use Firefox-family profiles on Firefox-family browsers

The runtime does not stop manual operators from making bad choices. Higher-level shells can do that if they want to.

---

## Request classification and protocol handling

STATIC's inbound routing now distinguishes between:

- direct TLS interception
- HTTP CONNECT proxy traffic
- plain HTTP proxy traffic

That matters because older descriptions often collapsed everything into one generic HTTP proxy story.

At runtime, the connection path then branches into the appropriate downstream and upstream handling path, including:

- HTTP/1.1 sessions
- HTTP/2 sessions
- raw websocket tunneling
- local runtime asset delivery for `__/static/runtime.js`-style support assets
- buffered HTML mutation only when response stages actually require it

---

## Deterministic stage pipeline

The current stage order is:

1. `HeaderProfileStage`
2. `BehavioralNoiseStage`
3. `CspStage`
4. `JsInjectionStage`
5. `AltSvcStage`

That order is important.

- profile shaping has to exist before runtime config is embedded
- CSP handling has to happen before the final injected script layout is sent
- Alt-Svc handling happens after the main mutation decisions are made

---

## Transport boundary

STATIC's transport plan is richer than the old "rewrite the handshake" phrasing suggested.

The real contract is closer to this:

- profile data describes the desired upstream transport shape
- STATIC passes that plan into the current fetcher/backend boundary
- actual wire fidelity is bounded by what the current backend can express

Current plan inputs include things like:

- cipher-suite ordering
- signature-algorithm ordering
- supported-group ordering
- ALPN
- extension ordering
- delegated credentials
- ALPS settings where applicable
- session-resumption controls

That is meaningful shaping, but it is not the same thing as promising exact packet parity with every target browser build on every stack.

---

## JS runtime model

The JS runtime is not a pile of unrelated patch files anymore.

It boots as a fixed pipeline with a shared registry and shared entropy state.

High-level bootstrap order:

1. runtime registry initialization
2. native reference capture
3. `Function.prototype.toString` masking
4. CSP nonce capture
5. config load and validation
6. entropy initialization
7. policy initialization
8. identity, capability, spoofing, evasion, privacy, and iframe modules

That structure matters because the runtime now tries much harder to keep surfaces coherent within one process lifetime instead of inventing unrelated randomness everywhere.

---

## Worker and iframe handling

Two details matter here:

### Workers

Worker and SharedWorker construction is wrapped through bootstrap scripts so STATIC can carry family and identity state into the worker path.

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

## Limits that still matter

The honest limits are still important:

- exact on-the-wire TLS parity is bounded by the current transport backend
- service workers and already-existing worker state remain outside the strongest injected-runtime path
- manual operators can still select incoherent family combinations if they insist on doing that
- STATIC and the eBPF layer are still distinct systems even when packaged together

Those are not edge disclaimers. They are part of the current reality and the docs should say so plainly.