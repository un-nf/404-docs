
## What is 404?

By leveraging a Blazing fast Rust privacy proxy & a Linux kernel module, 404 offers full control over your machine's fingerprint.

404 houses two main modules:
- STATIC Proxy - *Synthetic Traffic and TLS Identity Camouflage*
- Linux eBPF module

### STATIC Proxy
#### *Synthetic Traffic and TLS Identity Camouflage*

The heart of 404, built in Rust. 

> Native values from FingerprintJS ![here](.github/IMAGES/cleanChrome.png).

> Spoofed values from FingerprintJS ![here](.github/IMAGES/dirtyChrome.png).

*I want to start by saying I am new to the Rust ecosystem, If you see something I did wrong or could do better, open an issue.*

That being said, the STATIC proxy is built from the ground up and wired specifically to give the user granular control over their fingerprint. Not just their browser fingerprint, but any device or app they choose to route through the proxy.

As it stands in v1.0, STATIC runs on `localhost:4040` by default, never exposing itself to the internet or any device other than the one that it is running on. The logic behind STATIC is pretty simple and mimics a lot of the high-level logic that `mitmproxy` employs. 

Requests are broken into `flow`s. Each `flow` passes through multiple `stage`s. A `stage` is where the request/response mutation happens. 

**Request stages:**
1. **HeaderProfileStage** - Rewrites headers based on your selected profile (User-Agent, Accept, sec-ch-ua, Accept-Language). Maintains strict ordering to match real browser behavior: remove -> replace -> replaceArbitrary -> replaceDynamic -> set -> append.

2. **AltSvcStage** - Downgrades or strips HTTP/3 advertisements to prevent protocol leakage.

3. **CspStage** - Generates CSP nonces and rewrites Content-Security-Policy headers so injected scripts execute without breaking origin policies.

4. **JsInjectionStage** - Embeds the fingerprint spoofing stack (bootstrap, globals shim, config layer, spoof scripts) near `</head>` or `</body>`. Records SHA-256 hashes for CSP validation.

5. **BehavioralNoiseStage** - Tags the flow with timing patterns for coordination between Rust and injected JavaScript.

**Response stages:**
1. **CspStage (response)** - Finalizes CSP headers with script hashes and nonces, handles strict-dynamic policies, preserves origin inline scripts.

2. **JsInjectionStage (response)** - Performs the actual HTML mutation, decompresses responses if needed (gzip/deflate/brotli), injects scripts at the earliest safe insertion point.

3. **AltSvcStage (response)** - Strips or normalizes Alt-Svc headers in responses to prevent the browser from upgrading to HTTP/3.

Each stage runs asynchronously and can inspect or mutate the request/response. The pipeline is deterministic. Same profile, same mutations, same fingerprint.

Don't believe me? Check my work... 
1. https://demo.fingerprint.com/playground
2. https://browserleaks.com/
3. https://coveryourtracks.eff.org/
4. https://whatismybrowser.com/
5. https://httpbin.org/headers

### Linux eBPF module

The eBPF module is, again, quite simple. It leverages powerful, fast, well documented, low-level Linux kernel hooks. By attaching carefully crafted eBPF programs to Linux's Traffic Control (tc) egress hooks, we can mutate files extensively.

Currently, the following is implemented:
```md
**IPv4:**
- TTL (Time To Live) -> forced to 255
- TOS (Type of Service) -> set to 0x10
- IP ID (Identification) -> randomized per packet
- TCP window size -> 65535
- TCP initial sequence number -> randomized (again)
- TCP window scale -> 5
- TCP MSS (Maximum Segment Size) -> 1460
- TCP timestamps -> randomized

**IPv6:**
- Hop limit -> forced to 255
- Flow label -> randomized
```

---

## How do I install and run 404 on my machine?

### Requirements

> Utilizing the eBPF module requires a Linux kernel (4.15+).

| Component | Version | Install Link |
|-----------|---------|-------|
| **Rust** | 1.76+ | [INSTALL](https://rust-lang.org/tools/install/) - *manual install req.* |
| **CMake** | Latest | [INSTALL](https://www.nasm.us/pub/nasm/releasebuilds/3.01/) |
| **NASM** | Latest | [INSTALL](https://cmake.org/download/) |

Default install locations...
    - `C:\Program Files\NASM`
    - `C:\Program Files\CMake\bin`

### 1. Install dependencies & configure PATH

<details>
<summary><b>Windows</b></summary>

**Option 1: Install via winget (recommended)**

```powershell
# Install CMake
$ winget install Kitware.CMake

# Install NASM (interactive - choose installation directory when prompted)
$ winget install nasm -i
```

*Restart your shell after installation. Tools should be on your PATH automatically.*

**Option 2: Manual installation**

Add to PATH:

   - Search for "*edit environment*" in Windows search and open the control panel
   - Under `User variables for %USER%` click on `Path` then `Edit...`
   - Click `New` and add the paths to `NASM` and `CMake\bin`

Default install locations...
    - `C:\Program Files\NASM`
    - `C:\Program Files\CMake\bin`

</details>

<details>
<summary><b>macOS</b></summary>

**Install via `Homebrew`**

```bash
# Install Homebrew if you don't have it
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
$ brew install rust nasm cmake

# Rust, NASM, and CMake should be on your PATH automatically
```

</details>

<details>
<summary><b>Linux</b></summary>

**Install via package manager**

```bash
# Debian/Ubuntu
$ sudo apt update
$ sudo apt install -y curl build-essential nasm cmake

# Arch
$ sudo pacman -S rust nasm cmake

# Fedora/RHEL
$ sudo dnf install -y rust cargo nasm cmake

# Install Rust via rustup (if not installed via package manager)
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
$ source $HOME/.cargo/env
```

</details>

### 2. Run the proxy

```bash
$ cd 404/src/STATIC_proxy # Your path
$ cargo run   # This will take a while on the first run.
```

### 3. Trust proxy-generated CA

<details>
<summary><b>Windows</b></summary>

1. Navigate to the `404/` directory and locate the `../static_proxy/certs/` directory.

2. Double-click the file labeled `static-ca.crt` (may appear without .crt extension)

3. Click `Install Certificate...`

4. Select `Current User` and click `Next`

5. Choose `Place all certificates in the following store` and click `Browse...`

6. Select `Trusted Root Certification Authorities` and click `OK`

7. Click `Next` then `Finish`

</details>

<details>
<summary><b>macOS</b></summary>

```bash
# Open Keychain Access and import the CA
$ sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain static_proxy/certs/static-ca.crt

# Or use the GUI:
# 1. Open Keychain Access
# 2. File -> Import Items -> select static-ca.crt
# 3. Find the certificate, double-click it
# 4. Expand "Trust" and set "When using this certificate" to "Always Trust"
```

</details>

<details>
<summary><b>Linux</b></summary>

```bash
# Copy CA to system trust store
$ sudo cp static_proxy/certs/static-ca.crt /usr/local/share/ca-certificates/static-ca.crt
$ sudo update-ca-certificates

# For Firefox specifically (uses its own trust store):
# Open Firefox -> Settings -> Privacy & Security -> Certificates -> View Certificates
# -> Authorities tab -> Import -> select static-ca.crt
# -> Check "Trust this CA to identify websites" -> OK
```

</details>

**Configure your browser:**

Set your browser (or system) to use `localhost:8080` (or `127.0.0.1:8080`) as an HTTP/HTTPS proxy.

- **Chrome/Edge:** Settings -> System -> Open your computer's proxy settings
- **Firefox:** Settings -> Network Settings -> Manual proxy configuration -> HTTP Proxy: `127.0.0.1`, Port: `8080`, check "Also use this proxy for HTTPS"

***Important:*** **This tool is a TLS-terminating proxy (man-in-the-middle) and has access to your plaintext HTTPS data (usernames, passwords, certain message protocols, etc.). Do NOT share your CA cert with *anyone* for *anything, ever*.**

*UX on Firefox is slightly more stable for reasons that are not clear to me. Would love some insight. Login flows have been tested and are working in both browsers.*

### 4a. Compile & attach eBPF program to TC egress hook (if using Linux)

*The eBPF `ttl_editor` modifies packet-level fingerprints (TTL, TCP window size, sequence numbers, etc.). This requires a Linux kernel.*

![tcpdump output](.github/IMAGES/tcpdump_output.png)

**Kernel requirements:**

- CONFIG_BPF=y, CONFIG_BPF_SYSCALL=y, CONFIG_NET_CLS_BPF=y, CONFIG_NET_ACT_BPF=y
- Install: `clang`, `llvm`, `libbpf-dev`, `linux-headers-$(uname -r)`, `iproute2`

**Build eBPF program**
> Currently, IP/TCP packet header values are assigned via global variables at the top of `src/ebpf/ttl_editor.c`.

*Modify these to desired values *before* compiling.*

```bash
$ $ cd src/ebpf
$ make deps-install  # shows dependency installation command
$ make               # compiles ttl_editor.o
$ 
$ # Manual compilation
$ clang -O2 -g -target bpf -D__TARGET_ARCH_x86 -I/usr/include/ -I/usr/include/linux -c TTLEDIT-STABLE.c -o <output>.o

```

**Attach to network interface:**

```bash
$ sudo tc qdisc add dev <interface> clsact
$ sudo tc filter add dev <interface> egress bpf da obj ttl_editor.o sec classifier

```

### 4b. Configure a Linux VM (if not using Linux)

**VM Setup:**

> *VM images coming soon. I am using VMWare to host a Deb-Bookworm distribution. Works mildly well, but really heavy. Definitely going to be looking into distributing the VMs as dedicated server images, not gerry-rigged forwarding machines with desktop environments.*

You *100% could* configure a VM and route traffic from your host machine to a VM guest, [instructions for VM configuration here](docs/VMConfig.md).

For now, just running STATIC should be enough, though network level obfuscation is not possible without a Linux kernel (yet).