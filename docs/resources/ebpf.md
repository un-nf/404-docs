---
title: eBPF Guide
description: Technical reference for 404's eBPF module, including the current packet mutations, Linux requirements, build path, and where it fits relative to the desktop application and CLI application.
hide:
  - toc
---

# eBPF

!!! info "Current role"

    The eBPF layer is real and currently wired into the Linux runtime path.

    It is part of the open source CLI application and runtime toolchain, not a separate hosted service.

---

## What it does today

The current module attaches to Linux Traffic Control (`tc`) egress hooks and rewrites packet-level values that can be used for passive OS and stack fingerprinting.

Current implemented behavior:

```md
**IPv4:**
- TTL (Time To Live) -> forced to 255
- TOS (Type of Service) -> set to 0x10
- IP ID (Identification) -> randomized per packet
- TCP window size -> 65535
- TCP initial sequence number -> randomized
- TCP window scale -> 5
- TCP MSS (Maximum Segment Size) -> 1460
- TCP timestamps -> randomized

**IPv6:**
- Hop limit -> forced to 255
- Flow label -> randomized
```

---

## Where it fits

The eBPF layer is not a replacement for STATIC. It complements STATIC.

- STATIC handles TLS, HTTP, injected runtime shaping, and control-plane behavior.
- The eBPF layer handles lower-level packet mutation on Linux.

On Windows, the managed desktop product path reaches this Linux layer through the WSL2 runtime.

On CLI-managed Linux paths, you can build and attach it directly yourself.

---

## Kernel and toolchain requirements

You need a Linux environment with:

- Linux kernel `4.15+` (`5.4+` recommended)
- `clang`
- `llvm-strip`
- `tc`
- `/usr/include/bpf/bpf_helpers.h`
- `/usr/include/linux/bpf.h`

---

## Build path

The Makefile in `src/ebpf` builds:

- `ttl_editor.o`

Typical local invocation:

```bash
make -C src/ebpf clean all
```

This is the same object that is packaged into the WSL distro build path.

---

## Attach path

Typical attach sequence:

```bash
sudo tc qdisc add dev <interface> clsact
sudo tc filter add dev <interface> egress bpf da obj ttl_editor.o sec classifier
```

Removal:

```bash
sudo tc filter del dev <interface> egress
sudo tc qdisc del dev <interface> clsact
```

---

## Important limitation

The packet policy is still not fully profile-driven in the way the higher-level runtime is.

The broader product direction is to keep userspace identity and kernel-level mutation moving toward the same selected profile state, but you should not read the current implementation as fully live-reconfigurable parity yet.