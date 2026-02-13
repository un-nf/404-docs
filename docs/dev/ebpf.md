# eBPF Kernel Module

## Overview

![tcpdump output](../assets/images/tcpdump_output.png)

> The eBPF module modifies packet-level fingerprints (TTL, TCP window size, sequence numbers, etc.). This requires a Linux kernel.

## Kernel requirements:

- CONFIG_BPF=y, CONFIG_BPF_SYSCALL=y, CONFIG_NET_CLS_BPF=y, CONFIG_NET_ACT_BPF=y
- Install: `clang`, `llvm`, `libbpf-dev`, `linux-headers-$(uname -r)`, `iproute2`

---

## Configuration

> Currently, IP/TCP packet header values are assigned via global variables at the top of `src/ebpf/ttl_editor.c`. They *do not* align with values passed from `profiles.json`, this is a major pitfall of the current version and will be integrated with dynamic `bpfmaps` in a future release.

*Modify hardcoded globals to desired values before compiling.*

**Native OS Options:**
    
| OS | TTL | Window Size | Window Scale | ISN | MSS* | Timestamps | TCP Option Order |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| Windows | 128 | 64 kb (64240 bytes) | 8 | Randomized | Varies based on connection | Not used | MSS,NOP,WS,NOP,NOP,SACK |
| MacOS | 64 | 64 kb (65535 bytes) | 6 | Randomized | Varies based on connection | Internal counter | MSS,NOP,WS,NOP,NOP,TS,SACK,EOL |
| Linux | 64 | 64 kb (65535 bytes - 5840 bytes for 2.4/2.6 kernels) | 7 | Randomized | Varies based on connection | Internal counter - sometimes randomized | MSS,SACK,TS,NOP,WS |

??? note "Default Implementation Options"

    IPv4:
    
    - TTL (Time To Live) → forced to 255
    - TOS (Type of Service) → set to 0x10
    - IP ID (Identification) → randomized per packet
    - TCP window size → 65535
    - TCP initial sequence number → randomized (again)
    - TCP window scale → 5
    - TCP MSS (Maximum Segment Size) → 1460
    - TCP timestamps → randomized
    
    IPv6:
    
    - Hop limit → forced to 255
    - Flow label → randomized
    - TCP parameters (same as IPv4)

**1. Open `ttl_editor.c` and modify the `#define` values at the top:** *(optional)*

```c
#define FORCE_TTL 255
#define SPOOF_TCP_WINDOW_SIZE 65535
#define SPOOF_TCP_MSS 1460
#define SPOOF_TCP_WINDOW_SCALE 5
// etc.
```

---

## Build eBPF program

**1.**
```bash
cd src/ebpf
make deps-install  # shows dependency installation command
make               # compiles ttl_editor.o
 
# Manual compilation
clang -O2 -g -target bpf -D__TARGET_ARCH_x86 -I/usr/include/ -I/usr/include/linux -c TTLEDIT-STABLE.c -o <output>.o

```

---

## Attach to network interface:

**2.**
```bash
sudo tc qdisc add dev <interface> clsact
sudo tc filter add dev <interface> egress bpf da obj ttl_editor.o sec classifier

```

---

## Remove from interface

**3.**
```bash
sudo tc filter del dev <interface> egress
sudo tc qdisc del dev <interface> clsact

```

---

## Configure a Linux VM for forwarding

**Kernel requirements:**

- CONFIG_BPF=y, CONFIG_BPF_SYSCALL=y, CONFIG_NET_CLS_BPF=y, CONFIG_NET_ACT_BPF=y
- Install: `clang`, `llvm`, `libbpf-dev`, `linux-headers-$(uname -r)`, `iproute2`

- Linux kernel 4.15+ (5.4+ recommended)

**1. Ensure your VM has two network adapters:**

1. `Bridged` - connects `VM/Guest` to internet
2. `Host-Only` - creates private network between `Host` and `VM/Guest`

**2. Attach to network interface:**

```bash
sudo tc qdisc add dev <interface> clsact
sudo tc filter add dev <interface> egress bpf da obj ttl_editor.o sec classifier

```
**3. Route host traffic through VM:**

***On `Linux VM` (Guest):***

```bash
# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -w net.ipv6.conf.all.forwarding=1
echo "net.ipv6.conf.all.forwarding=1" | sudo tee -a /etc/sysctl.conf

# Allow forwarding on Host-Only interface
sudo iptables -A FORWARD -i <host-only-interface> -j ACCEPT
sudo iptables -A FORWARD -o <host-only-interface> -j ACCEPT
sudo ip6tables -A FORWARD -i <host-only-interface> -j ACCEPT
sudo ip6tables -A FORWARD -o <host-only-interface> -j ACCEPT

# Enable NAT/masquerading on Bridged interface
sudo iptables -t nat -A POSTROUTING -o <bridged-interface> -j MASQUERADE
sudo ip6tables -t nat -A POSTROUTING -o <bridged-interface> -j MASQUERADE
```

***On Host machine:***

- Set default gateway to `VM/Guest` Host-Only adapter IP address
- (Windows: Network adapter settings → Properties → TCP/IPv4 → Gateway)
- (Linux/Mac: `sudo route add default gw <vm-host-only-ip>`)

> Some additional tinkering may be required. Feel free to leave a comment or open an issue with suggestions on improving the setup process.

---

## Verify & Test

**1. Verify it's running:**

```bash
sudo tc filter show dev <interface> egress
```

**2. Verify w/ tcpdump output, some examples below:**

```bash
tcpdump -i <interface> -vvv -Q out

# View specific TCP/IP fields:
tcpdump -i <interface> -vvv -c 20 -Q out 'tcp[tcpflags] & tcp-syn != 0'  # SYN packets only (-c for 20 packets)
tcpdump -i <interface> -vvv -nn -Q out | grep -E 'ttl|win|mss|wscale'  # Filter for specific fields

# More detailed packet inspection:
tcpdump -i <interface> -vvv -XX -Q out  # Show full hex dump
tcpdump -i <interface> -vvv -Q out port 443  # HTTPS traffic only
```

---

## Why eBPF?

eBPF programs run in the kernel with strict safety guarantees enforced by the verifier. This program:

1. Attaches to a network interface's TC egress hook
2. Inspects every outgoing packet
3. Modifies packet headers in-place (TTL, TCP options, etc.)
4. Recalculates checksums where necessary
5. Passes the modified packet onwards
6. The verifier ensures the program can't crash the kernel, access arbitrary memory, or run forever. All bounds checks are verified at load time.

Operating systems have distinct network stack implementations. Windows, Linux, macOS, Android, and iOS set different default values for TCP/IP packet headers (TTL, MSS, WinSize/Scale). These fingerprinting vectors are trivial to collect and can identify your OS even if you spoof your HTTP headers and browser fingerprint perfectly. Tools like nmap and p0f allow third party network observers to exploit this fingerprinting vector.

> Mismatches between network, JS, and HTTPS values can also be used by servers to identify bot-likely traffic and block connections.

Tools like p0f and nmap can passively fingerprint an OS by analyzing these packet-level characteristics. This eBPF program attempts to normalize these values to make passive fingerprinting harder.
