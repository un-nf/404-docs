---
title: API Documentation
description: Reference for STATIC's localhost control plane, including authentication, status routes, CA lifecycle routes, profile endpoints, and the current desktop integration contract.
hide:
  - toc
---

# Control Plane and API

!!! tip "STATIC has an authenticated localhost control plane that the [desktop app](https://404privacy.com/product/) uses"

---

## Bind and port rules

The control plane binds on:

```text
listener.bind_port + 2
```

---

## Authentication

When `control.token_path` is configured, STATIC reads a shared token from disk and requires it on control routes via:

```text
X-404-Control-Token
```

!!! info "Unauthenticated control"
    
    If no token path is configured, the control plane can run without that header on a local-only path. The desktop app does not share that functionality.

---

## API endpoints

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

## Important notes

### `GET /status`

Use this to confirm:

- Runtime mode
- Process readiness

### `GET /ca/status`

Returns:

- Certificate PEM
- Managed CA certificate path
- Whether the certificate exists

### `POST /ca/init`

Initializes CA material if needed and returns the same response shape as `GET /ca/status`.

### Profile routes

- `GET /profiles/catalog` exposes the discovered profile catalog plus the active profile
- `GET /profiles/active` exposes the selected profile only
- `POST /profiles/select` changes the in-memory active profile
- `POST /profiles/validate` returns profile-coherence warnings for candidate profile data

---

## Desktop integration

The desktop app relies on the control plane for:

- Readiness and lifecycle
- CA bootstrap and CA status
- Telemetry snapshots
- Active profile reads
- Profile validation

!!! example "Roadmap item"

    The desktop app does **not** fully consume the catalog and selection endpoints yet. The control plane is ahead of the desktop UI here.

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

## Limitations

The control plane is still a host-coupled service contract. It is not yet a polished standalone operator API with stable public compatibility.

!!! example "Roadmap item"

    API changes will be noted in release notes located [here](https://github.com/un-nf/404/tree/main/.REL_notes).