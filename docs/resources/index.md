---
title: Deep Reference
description: Technical reference entry point for the STATIC runtime, control plane, profile model, eBPF layer, and repository boundaries.
hide:
  - toc
---

# Deep Reference

This section is for readers who want the implementation-facing view rather than the setup path.

Use it when you need to answer questions like:

- what does STATIC actually promise today
- which defaults are real and which ones are legacy leftovers
- how does the localhost control plane work
- what is profile state versus runtime policy versus seeded persona materialization
- what exactly is packaged into the WSL runtime path

---

## Reference map

- [STATIC Runtime and Data Plane](./static.md)
- [Control Plane and CA State](./controlPlane.md)
- [Profiles and Persona Materialization](./profiles.md)
- [eBPF Reference](./ebpf.md)
- [Runtime Repository Map](./repoDev.md)

---

## Scope

These pages are deliberately narrower and more exact than the getting-started docs.

They try to stay close to the current source tree, release workflows, and runtime contracts instead of repeating older broad explanations that no longer describe the live system cleanly.