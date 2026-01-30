---
title: 404 Proxy
description: Reclaim your digital anonymity with a local-first spoofing proxy for TLS, headers, and fingerprint surfaces.
hide:
  - toc
---
# 404 - Home

## Reclaim Your **Digital Anonymity**

*Stealth by design. Illegibility on purpose.*

!!! info "v1.1 available"
    New builds are live. If you’re upgrading, skim the release notes before swapping profiles.

[Get Started](Overview/consent.md){ .md-button .md-button--primary }
[GitHub](https://github.com/un-nf/404){ .md-button }

---

## Core capabilities

-   ### Anti-fingerprinting
    404 targets *correlation*: offers coherent profiles across **TLS → headers → JS surfaces**.

-   ### Cross-platform
    Written in Rust for **Windows, macOS, Linux**. Run locally, keep control locally.

-   ### Open source
    Full transparency.

---

## The leakage problem

Your browser is telling ad-tech corporations **too much**.

Websites and fingerprinting vendors collect semi-unique signals and combine them into a “personality cloud”:

- Canvas and text rendering quirks  
- WebGL parameters and GPU hints  
- Audio context characteristics  
- Fonts and device enumeration  
- Locale/timezone/screen geometry  
- TLS and header shapes
- Typing speed

404 sits in the middle and **rewrites your fingerprint** before it leaves your machine.

---

## The “personality cloud” (before / after)

```mermaid
flowchart LR
  %% Zig-zag layout: left -> middle -> right
  A["BROWSER_SIGNAL<br/><b>[LEAKING]</b><br/><br/>User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) …<br/>CanvasID: 9b:17:2f:aa:…<br/>WebGL: ANGLE (Apple, Apple M1, OpenGL 4.1)<br/>Fonts: 178 enumerated<br/>TLS: ClientHello shape: unique-ish"]

  B["404_PROXY<br/><b>[INTERCEPT]</b><br/><br/>• rewrite TLS plan<br/>• normalize headers + ordering<br/>• inject JS spoofing stack (profile JSON)<br/>• block/downgrade leaky upgrades (when configured)"]

  C["SPOOFED_SIGNAL<br/><b>[PROTECTED]</b><br/><br/>User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) …<br/>CanvasID: 0xFD42… (scrambled deterministically)<br/>WebGL: NVIDIA… (profile-consistent)<br/>Fonts: constrained + salted<br/>TLS: profile-aligned handshake shape"]

  A -->|HTTPS request| B -->|rewritten request| C

  classDef leak fill:#2b1b1b,stroke:#ff6b6b,stroke-width:1px,color:#ffdede;
  classDef mid  fill:#1b2433,stroke:#4b8bff,stroke-width:1px,color:#dbe9ff;
  classDef safe fill:#1b2b1f,stroke:#4ade80,stroke-width:1px,color:#dcffe7;

  class A leak;
  class B mid;
  class C safe;

```

---

## What 404 changes

#### **TLS handshake**

404 controls handshake behavior *as a profile decision*: extensions, ordering, ALPN, key shares, and cipher preferences are defined in the profile.

!!! note
    TLS impersonation fidelity is adversarial and evolving. The goal is **plausible identity**.

#### **HTTP + HTTP/2**

Normalizes and rewrites headers and header ordering to match the chosen persona.

- Consistent `User-Agent` + client hints  
- Language/timezone coherence  
- Optional downgrades/strips to reduce leak paths (e.g., `Alt-Svc` preventing accidental HTTP/3/QUIC identity drift)

#### **JavaScript fingerprint surfaces**

Injects a profile-driven spoofing layer (canvas/WebGL/audio/fonts/media devices, etc.) while keeping the identity coherent.

!!! tip
    Coherence beats randomness. Random noise is how you become a rare, clusterable outlier.

---