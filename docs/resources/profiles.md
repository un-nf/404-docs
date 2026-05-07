---
title: Profiles and Persona Materialization
description: Technical reference for STATIC's profile catalog, family-first identity model, seeded overlays, startup selection rules, and the split between manual operator choice and higher-level desktop policy.
hide:
  - toc
---

# Profiles and Persona Materialization

STATIC is no longer built around a vague idea of "pick a browser string and spoof some values."

The current runtime is profile-driven all the way through startup, validation, transport shaping, and injected runtime state.

---

## What a profile does now

A current runtime profile can contribute:

- identity metadata such as family, variant, and platform
- header shaping rules
- runtime fingerprint config
- TLS and HTTP/2 behavior hints
- seeded overlay choices that materialize into one concrete persona for the lifetime of the process

That last point matters. The runtime is not just loading a JSON file and reading values lazily. It materializes a process-lifetime persona and keeps that in memory.

---

## Current bundled profile families

The shipped runtime path is currently organized around browser families rather than cross-engine fantasy.

Best practice:

- Chromium-family browsers should use Chromium-family profiles
- Firefox-family browsers should use Firefox-family profiles

STATIC does not hard-enforce that policy for manual operators. That is intentional.

The lower-level runtime stays flexible. Higher-level wrappers can be stricter if they want to prevent obviously incoherent choices.

---

## Startup rules

Proxy mode does not silently start in an ambiguous state anymore.

The active profile must come from one of these places:

- `--profile <name>`
- `pipeline.default_profile` in config

If neither exists, proxy mode stops rather than guessing.

That change is load-bearing. It prevents the runtime from starting in a state where transport and JS shaping have no explicit identity basis.

---

## Shared profile state

The current runtime loads one shared `ProfileStore` and uses it in both:

- the data plane
- the localhost control plane

That is what makes runtime profile reads and runtime profile updates coherent.

Without that shared in-memory state, the control plane and proxy pipeline drift apart.

---

## Seeded overlays

Some profiles contain `seeded_overlays`.

Those overlays are not meant to be re-rolled on every request.

They are materialized into one concrete persona for the lifetime of the process, then recorded as the selected overlay state the runtime actually uses.

That gives the runtime:

- stable per-process identity
- internally consistent high-entropy values
- rotation on restart instead of noisy within-session drift

---

## What the control plane exposes

The catalog endpoints expose profile metadata suitable for higher-level clients:

- key
- display name
- family
- variant
- platform

That is enough for the desktop shell to present compatible choices without needing to re-parse every profile file itself.

---

## What a profile is not

A profile is not a guarantee that the underlying transport backend can emit every requested wire shape exactly.

That distinction matters most for TLS.

The profile can describe the desired transport plan, but actual wire fidelity is still bounded by what the current Rust-side transport backend can express.

That is why warnings and validation exist. The profile model can be richer than the current transport emitter.