---
title: Profiles
description: Technical reference for STATIC's profile catalog, family-first identity model, seeded overlays, and startup selection rules.
hide:
  - toc
---

# Profiles and Persona Materialization

STATIC is profile-driven through startup, validation, transport shaping, and injected runtime state.

---

## What a profile defines

- Identity metadata such as family, variant, and platform
- Header shaping rules
- Runtime fingerprint config
- TLS and HTTP/2 behavior hints
- Seeded overlay choices that materialize into one concrete persona for the lifetime of the process

---

## Profile families

The shipped runtime path is organized around browser families and discourages cross-engine spoofing.

Best practice:

- Chromium-family browsers should use Blink-family profiles
- Firefox-family browsers should use Gecko-family profiles

!!! Warning "Neither STATIC nor the Rose base enforces this policy."

---

## Startup rules

Proxy mode does not silently start in an ambiguous state anymore.

The active profile must come from one of these places:

- `--profile <name>`
- `pipeline.default_profile` in config

!!! warning "If neither exists, STATIC will not run."

---

## Shared profile state

The current runtime loads one shared `ProfileStore` and uses it in both the data plane and the localhost control plane

That is what makes runtime profile reads and runtime profile updates coherent.

Without that shared in-memory state, the control plane and proxy pipeline drift apart.

---

## Seeded overlays

Some profiles contain `seeded_overlays`.

Those overlays give the runtime:

- Stable per-process identity
- Internally consistent high-entropy values
- Rotation on restart instead of noisy within-session drift

---

## [Control plane](./controlPlane.md)

The catalog endpoints expose profile metadata suitable for higher-level clients:

- Key
- Display name
- Family
- Variant
- Platform