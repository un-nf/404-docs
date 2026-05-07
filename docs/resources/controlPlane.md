---
title: Control Plane and CA State
description: Technical reference for STATIC's localhost control plane, including authentication, status routes, CA lifecycle routes, profile endpoints, and the current desktop integration contract.
hide:
  - toc
---

# Control Plane and CA State

STATIC no longer behaves like a single opaque proxy process with no operator surface.

It has an authenticated localhost control plane that the desktop app already uses on the live path.

---

## Bind and port rules

The control plane binds on:

```text
listener.bind_port + 2
```

That means:

- sample config listener `4040` -> control plane `4042`
- standalone CLI default listener `8443` -> control plane `8445`

HTTP/3 is a separate listener concept. It is **not** the control plane.

---

## Authentication model

When `control.token_path` is configured, STATIC reads a shared token from disk and requires it on control routes via:

```text
X-404-Control-Token
```

If no token path is configured, the control plane can run without that header on a local-only operator path. The desktop app does not rely on that weaker mode.

---

## Current routes

The current control plane exposes:

- `GET /status`
- `GET /ca/status`
- `POST /ca/init`
- `POST /stop`
- `GET /telemetry/snapshot`
- `GET /profiles/catalog`
- `GET /profiles/active`
- `POST /profiles/select`
- `POST /profiles/validate`

---

## What matters most in practice

### `GET /status`

Use this to confirm:

- runtime mode
- whether the process currently considers itself ready

### `GET /ca/status`

Returns:

- the managed CA certificate path
- whether the certificate exists
- the certificate PEM itself

This is what makes the current host-trust bridge workable. The Linux runtime keeps private key custody, but the desktop app can still retrieve the public certificate material it needs to install trust on the host.

### `POST /ca/init`

Initializes CA material if needed and returns the same response shape as `GET /ca/status`.

### Profile routes

These are now part of the real runtime state model, not a future idea.

- `GET /profiles/catalog` exposes the discovered profile catalog plus the active profile
- `GET /profiles/active` exposes the selected profile only
- `POST /profiles/select` changes the in-memory active profile
- `POST /profiles/validate` returns profile-coherence warnings for candidate profile data

---

## Desktop integration status

The desktop app already relies on the control plane for:

- readiness and lifecycle
- CA bootstrap and CA status
- telemetry snapshots
- active profile reads
- profile validation

It does **not** fully consume the catalog and selection endpoints yet. That matters because the control plane is ahead of the desktop UI in this area.

---

## CA storage model

Current rule:

- the runtime owns CA generation and private key custody
- the host-facing app owns trust installation into the OS

The private key does not need to leave the runtime for host trust to work.

That is one of the main reasons the control plane returns `cert_pem` directly.

---

## Manual operator example

If you are running STATIC directly with a control token configured, a typical local check looks like:

```bash
TOKEN="$(cat /path/to/control.token)"
curl \
  -H "X-404-Control-Token: $TOKEN" \
  http://127.0.0.1:4042/status
```

Replace `4042` with whatever your actual control port is.

---

## Current limitation

The control plane is local and useful, but it is still a host-coupled service contract. It is not yet a polished standalone operator API with a stable public compatibility story documented version by version.

That is why higher-level compatibility and contract-version policy still belongs in release planning rather than being overstated here.