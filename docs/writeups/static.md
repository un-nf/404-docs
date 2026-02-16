---
title: STATIC Proxy Guide
description: Complete technical reference for STATIC proxy—architecture, TLS fingerprinting, HTTP/2 handling, profile configuration, and troubleshooting guide.
hide:
---

# STATIC Proxy

**A ground-up Rust implementation of a fingerprint-resistant MITM proxy**

!!! warning "Deep Dive Ahead"
    This page is designed for developers, researchers, and anyone who wants to understand *how* STATIC works under the hood. If you're just looking to get started, check out the [Getting Started](../dev/downloadDev.md) guide instead.

---

## What does STATIC do?

Modern fingerprinting is a **multi-layer problem**. Spoofing just your User-Agent or randomizing canvas values creates incoherent, *identifiable* noise. STATIC exists because defeating commercial fingerprinting requires **full-stack control**.

**TLS Layer**

- Rewrites the `SYN-ACK` handshake: cipher order, extensions, key shares
- Deterministic profile selection via `rustls` - non-robust
- JA3/JA4 string generation and validation

**HTTP Layer**

- Native HTTP/1.1 and HTTP/2 protocol parsing
- Header ordering, client hints, Accept negotiation

**JavaScript Layer**

- CSP nonce generation synchronized with injection
- Canvas/WebGL/Audio fingerprint spoofing
- Iframe boundary propagation
- Behavioral noise coordination between Rust and JS

**Async-Native Rust Architecture**

- **Tokio-based** concurrency (no thread pools, no blocking IO)
- **Zero-copy buffers** with `BytesMut`
- **Per-flow state isolation** (no global locks in hot path)
- **Structured telemetry** with `tracing` (JSON export ready)

---

## Architecture

??? Example "Repository Map"

    ```
    static_proxy/
    ├── Cargo.toml                      # Dependencies: tokio, rustls, h2, hyper, serde
    │
    ├── assets/js/                      # Embedded fingerprint spoofing scripts
    │   ├── 0bootstrap.js                  # Execution control, eval/Function wrapping
    │   ├── 1globals_shim.js               # Navigator/screen property interception
    │   ├── 2fingerprint_spoof_v2.js       # Canvas, WebGL, audio, font spoofing
    │   ├── behavioral_noise.js            # Coordinated timing/interaction patterns
    │   └── config_layer.js                # Profile injection into JS context
    │
    ├── config/
    │   └── static.example.toml         # Listener, TLS, pipeline, telemetry config
    │
    ├── profiles/                       # JSON profiles (Chrome/Firefox/Edge)
    │   ├── chrome_latest.json             # Schema v2: headers, TLS, behavior
    │   ├── firefox_latest.json
    │   └── safari_latest.json
    │
    ├── src/
    │   ├── main.rs                     # CLI entrypoint (clap args, tracing init)
    │   ├── app.rs                      # Wires subsystems, spawns listener
    │   │
    │   ├── proxy/                      # Core proxy logic
    │   │   ├── server.rs                  # TCP listener, protocol detection
    │   │   ├── connection.rs              # CONNECT handling, TLS termination, HTTP dispatch
    │   │   ├── flow.rs                    # Request/response/metadata container
    │   │   ├── pipeline.rs                # Stage orchestration trait
    │   │   ├── client.rs                  # Upstream dialer (TCP+TLS with profile plans)
    │   │   └── stages/                    # HeaderProfile, CSP, JS, AltSvc, Behavioral
    │   │
    │   ├── tls/                        # TLS subsystem
    │   │   ├── cert.rs                    # CA generation, leaf cert cache (DashMap)
    │   │   ├── profiles.rs                # TLS planner (JA3/JA4, cipher/group selection)
    │   │   ├── fingerprint.rs             # JA3 string computation for telemetry
    │   │   └── handshake.rs               # rustls ServerConfig/ClientConfig builders
    │   │
    │   ├── config/                     # Configuration system
    │   │   ├── settings.rs                # StaticConfig struct, TOML deserialization
    │   │   └── profiles.rs                # Profile loader with hot reload (notify crate)
    │   │
    │   ├── behavior/                   # Behavioral noise engine
    │   ├── assets.rs                   # Embedded JS files, SHA-256 precomputation
    │   ├── telemetry.rs                # Structured logging (JSON mode, tracing spans)
    │   └── utils/                      # Error types, logging helpers
    │
    └── tests/
        ├── unit/tls_tests.rs              # JA3 serialization, cipher filtering
        └── integration/proxy_tests.rs     # End-to-end flow validation

    ```

---

## Configuration

STATIC reads configuration from `config/static.toml` (or via `--config` flag). The config file is broken into logical sections that control different subsystems.

### **Listener**

Controls where STATIC binds and listens for incoming connections.

```toml
[listener]
addr = "127.0.0.1"
port = 4040

[http3]
enabled = false
bind_address = "127.0.0.1"
bind_port = 8081
```

??? warning "HTTP/3 Status"
    HTTP/3 configuration exists but is not yet implemented. STATIC currently handles HTTP/1.1 and HTTP/2 only. When enabled, this will spawn a QUIC listener using `quinn`.

### **TLS**

Defines paths for CA management and certificate caching.

```toml
[tls]
ca_cert_path = "certs/static-ca.crt"
ca_key_path = "certs/static-ca.key"
cache_dir = "certs/cache"

```

**What happens here:**

- On first run, STATIC generates a CA certificate and private key
- Private `.key` file is stored securely, implementation varies per OS
- Leaf certificates (for individual domains) are cached in `cache_dir`
- Cached certs have a 24-hour TTL and are validated on lookup

### **Pipeline**

Controls profile loading, injection behavior, and protocol handling.

```toml
[pipeline]
profiles_path = "../profiles"
default_profile = "firefox-windows"
js_debug = false
alt_svc_strategy = "normalize"
```

| Field | Options | Purpose |
|-------|---------|---------|
| `profiles_path` | Path to JSON profiles | Where STATIC looks for profile definitions |
| `default_profile` | Profile name | Fallback if no profile is selected or profile load fails |
| `js_debug` | `true`/`false` | Enables verbose JS console output in injected scripts |
| `alt_svc_strategy` | `normalize`, `strip`, `passthrough` | How to handle Alt-Svc headers (HTTP/3 downgrade behavior) |

### **Telemetry**

Configures logging output format and destination.

```toml
[telemetry]
mode = "stdout"

```

| Mode | Output |
|------|--------|
| `stdout` | Pretty-printed logs to console |
| `json` | Structured JSON logs (Loki/ELK ready) |

Use `RUST_LOG` environment variable to control verbosity:

```bash
# Human-readable logs
cargo run

# JSON structured logs
cargo run -- --json-logs

# Debug everything
RUST_LOG=static_proxy=debug cargo run

# Trace TLS subsystem only
RUST_LOG=static_proxy::tls=trace cargo run
```

---

## Data Plane

The data plane handles live traffic: protocol detection, TLS termination, request/response mutation, and upstream forwarding.

### Protocol Detection

STATIC peeks at incoming TCP connections to determine what it's dealing with:

| First Bytes | Protocol | Handler |
|-------------|----------|---------|
| `CONNECT` | HTTP CONNECT tunnel | `handle_connect_tunnel` |
| `0x16` | Direct TLS ClientHello | `accept_tls_session` |
| `GET`/`POST`/etc | HTTP/1.1 request | `handle_http1_session` |

#### CONNECT Handling

1. Parse `CONNECT host:port HTTP/1.1` from raw TCP stream
2. Validate hostname (no IP literals, no malformed targets)
3. Respond with `200 Connection Established\r\n\r\n`
4. Record target in `FlowMetadata.connect_target` for upstream resolution

#### TLS Termination

- Uses `tokio_rustls::TlsAcceptor` with on-demand certificate generation
- Extracts SNI from `ServerConnection::server_name()` (rustls 0.23 API)
- Falls back to `connect_target` when SNI is missing (rare, but happens)
- Generates leaf certificate signed by STATIC CA, caches in `DashMap<String, CachedCert>`

### Flow Model

A `Flow` represents a complete HTTP exchange.

**Structure:**

```rust
pub struct Flow {
    id: Uuid,                         // UUID v7 for deterministic ordering
    request: RequestParts,            // Headers, method, URI, body buffer
    response: Option<ResponseParts>,  // Populated after upstream response
    metadata: FlowMetadata,           // Profile, TLS, telemetry state
    behavioral_noise: BehavioralNoiseMetadata,
    fingerprint_config: Value,        // Profile JSON for JS injection
    timers: Timers,                   // Start, stage durations
    tls_plan: Option<TlsClientPlan>,  // Upstream TLS handshake instructions
}
```

**FlowMetadata** bridges network stack, pipeline, and telemetry:

- TLS SNI and CONNECT target
- Profile names (header + TLS + behavioral)
- CSP nonces and script SHA-256 hashes
- JA3/JA4 strings (computed from TLS plan)
- Upstream protocol (HTTP/1.1 vs HTTP/2)
- Stage mutation logs (breadcrumb trail for telemetry)

!!! tip "Performance"
    Buffers use `BytesMut` for zero-copy mutations during pipeline stages. Headers are reordered in-place without allocating new structures.

### Pipeline

**Execution order** is deterministic:

```
1. HeaderProfileStage
   └─ User-Agent, sec-ch-ua, Accept-Language
   └─ Order: remove → replace → replaceArbitrary
            → replaceDynamic → set → append

2. AltSvcStage
   └─ Downgrade/strip HTTP/3 advertisements
   └─ Normalize port lists

3. CspStage
   └─ Inject CSP nonces
   └─ Rewrite headers to allow injected JS

4. JsInjectionStage
   └─ Embed bootstrap + shim + config + spoof
   └─ Record SHA-256 hashes

5. BehavioralNoiseStage
   └─ Tag flow with noise plan
   └─ Coordinate with JS timing patterns

```

Each stage implements async hooks:

- `process_request` — Mutates outgoing request before upstream
- `process_response_headers` — Mutates headers before body processing
- `process_response_body` — Mutates HTML/JS content
- `on_complete` — Cleanup, telemetry emission

#### HeaderProfileStage

Applies header transformations from the profile's `headers` block.

**Operations (in order):**

1. **remove** — Delete headers by name (case-insensitive)
2. **replace** — Overwrite existing headers
3. **replaceArbitrary** — Replace with randomized values from a list
4. **replaceDynamic** — Template-based replacement (e.g., timestamp injection)
5. **set** — Add if missing, overwrite if present
6. **append** — Add to existing value or create new header

**Why ordering matters:**

Header order is part of the fingerprint. Real browsers send headers in a specific sequence. STATIC preserves that order from the profile.

#### AltSvcStage

HTTP/3 is a fingerprint leak. If your browser advertises `h3` support but your TLS fingerprint doesn't match a browser that supports HTTP/3, you're identifiable.

**Strategies:**

- **normalize** — Rewrite `Alt-Svc` to only advertise HTTP/2
- **strip** — Remove `Alt-Svc` headers entirely
- **passthrough** — Leave them alone (not recommended)

#### CspStage

Content Security Policy headers restrict which scripts can execute. STATIC injects JavaScript, so it needs to rewrite CSP headers to whitelist itself.

**How it works:**

1. Generate a per-flow `nonce` (cryptographically random, base64-encoded)
2. Compute SHA-256 hashes of injected scripts (precomputed at compile time)
3. Parse existing CSP headers from the response
4. Add `'nonce-<value>'` and `'sha256-<hash>'` to `script-src` directive
5. Preserve `'strict-dynamic'` if already present (common in modern CSP policies)

**CSP determinism:**

Script load order matters. STATIC always injects in the same order (0bootstrap → 1globals_shim → config_layer → 2fingerprint_spoof_v2 → behavioral_noise) to ensure CSP hashes remain valid.

#### JsInjectionStage

Embeds the fingerprint spoofing stack into HTML responses.

**Injection point:**

- Near `</head>` (preferred)
- Near `</body>` (fallback)
- Synthesize `<head>` if missing (rare, but handles malformed HTML)

**Injected scripts:**

```html
<script nonce="generated-nonce">
// 0bootstrap.js — Execution control, prevents double-injection
</script>
<script nonce="generated-nonce">
// 1globals_shim.js — Intercepts navigator/screen/window properties
</script>
<script nonce="generated-nonce">
// config_layer.js + profile JSON — Writes __STATIC_CONFIG__
</script>
<script nonce="generated-nonce">
// 2fingerprint_spoof_v2.js — Canvas/WebGL/Audio/Font spoofing
</script>
<script nonce="generated-nonce">
// behavioral_noise.js — Timing patterns, coordinated with Rust
</script>
```

**Decompression:**

Responses may be gzip/deflate/brotli-encoded. STATIC decompresses, injects, and re-compresses (or strips `Content-Encoding` and updates `Content-Length`).

#### BehavioralNoiseStage

!!! warning "Experimental feature, not fully implemented!"

Tags flows with timing patterns and interaction metadata. The JavaScript layer reads these patterns and coordinates behavior (e.g., randomized delays, simulated mouse movements).

**Rust side:**

- Parses behavioral strategies from profile JSON
- Writes metadata to `Flow.behavioral_noise`
- Marks flow as `behavioral_noise.enabled`

**JavaScript side:**

- Reads `__STATIC_CONFIG__.behavioral_noise`
- Annotates outgoing requests with timing metadata
- Modifies DOM interactions to avoid deterministic patterns

### HTTP/1.1 Engine

**Flow** (`connection.rs::handle_http1_session`):

```
parse_http_request (chunked decoder normalizes to contiguous buffer)
         ↓
Stage pipeline mutates request
         ↓
Upstream connect/dial
         ↓
send_request_to_upstream()
         ↓
parse_http_response (buffer complete response)
         ↓
Stage pipeline mutates response
         ↓
send_response_to_client()
```

**Edge cases handled:**

- **Bodyless status codes** (1xx/204/205/304) — Skip Content-Length validation to avoid hangs
- **Chunked encoding** — Normalize to contiguous buffer for pipeline processing
- **Connection: close** — Properly tear down TCP stream after response

!!! warning "Limitation: Streaming Bodies"
    HTTP/1 engine currently buffers entire request/response. Large uploads/downloads may pressure memory. Streaming support is planned.

### HTTP/2 Engine

**Flow** (`connection.rs::handle_http2_session`):

- Leverages `h2::server` for client-side HTTP/2 framing (ALPN `h2`)
- Each incoming stream spawns `process_http2_stream()` for per-request state isolation

**Upstream branching:**

- **`forward_h2_over_h2()`** — When origin negotiates HTTP/2 (ALPN `h2`)
- **`forward_h2_via_http1()`** — Fallback when upstream ALPN lacks `h2`

**Response handling:**

- Buffers complete headers/body before running response stages
- `sanitize_response_headers_for_h2()` removes hop-by-hop headers (`Connection`, `Transfer-Encoding`, etc.)
- Enforces `Content-Length`, normalizes lowercase header names (HTTP/2 spec requirement)

**Flow control:**

- `RecvStream::flow_control().release_capacity()` per chunk
- Prevents zero-window deadlocks
- 10-second timeout guard prevents hung upstream from blocking client

**Pseudo-header validation:**

HTTP/2 requires pseudo-headers (`:method`, `:scheme`, `:authority`, `:path`) at the start of the header block. STATIC enforces this on both request and response sides.

### HTTP/3 Roadmap

`Http3Config` already exists in `StaticConfig`. Implementation pending:

- `proxy::quic` module built on `quinn`
- CONNECT-UDP handler (RFC 9298)
- ALPS serialization within TLS planner
- Telemetry labels for H3 flows

---

## Limitations

STATIC is powerful but has known limitations. These are being actively worked on.

### TLS Coverage

**Missing from rustls/aws-lc:**

- **RSA key exchange** — Only ECDHE is supported
- **GREASE ciphers/extensions** — Rustls doesn't support GREASE values
- **Post-quantum hybrid key shares** — PQ crypto support is experimental

!!! warning 
    JA3 limited to ECDHE suites until BoringSSL integration is complete. Some browser profiles (older Safari, Edge) cannot be fully emulated.

### HTTP/3

**Status:** Config + roadmap exist, but no QUIC listener yet.

**Current behavior:** TLS planner clamps ALPN to `['h2','http/1.1']`.

**Planned:**

- `proxy::quic` module built on `quinn`
- CONNECT-UDP handler (RFC 9298)
- ALPS serialization for TLS 1.3

### Streaming Bodies

**HTTP/1 engine** buffers entire request/response in memory.

**Impact:** Large uploads/downloads (>100MB) may pressure memory and cause high latency.

**Planned:** 

- Streaming pipeline with chunked rewriter and stage API adjustments (stages would operate on body chunks instead of complete buffers).

### Connection Pooling

**Current behavior:**

- Upstream dials fresh TCP/TLS per request
- No keepalive/persistent connections
- No configurable timeouts

**Impact:** Higher latency, more TLS handshakes, easier to fingerprint by timing patterns.

**Planned:**

- Connection pool with keepalive (idle timeout, max connections per host)
- Configurable dial/read/write timeouts
- Happy Eyeballs DNS resolution (parallel IPv4/IPv6)

### DNS Caching

**Minimal caching** implemented. Relies on OS resolver (`tokio::net::lookup_host`).

**Planned:** 

- Happy Eyeballs with internal DNS cache (reduce resolution latency, improve consistency).

---