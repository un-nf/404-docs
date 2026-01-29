# Getting Started

!!! Info 
    All steps assume that there is a folder named `404` located at `%USERPROFILE%/git/404/`

## Run the proxy

Linux/macOS:

```bash
$ cd ~/git/404/src/STATIC_proxy # CHANGE to wherever you unzipped the 404 folder.
$ cargo run  # This will take a while on the first run (~5-minutes)
```

Windows:

```bash
$ cd %USERPROFILE%/git/404/src/STATIC_proxy # CHANGE to wherever you unzipped the 404 folder.
$ cargo run  # This will take a while on the first run (~5-minutes)
```

## Trust proxy-generated CA

??? note "Firefox"

    **Firefox uses its own trust store, you must trust the CA in the application:**

    !!! success ""
        Firefox -> Settings -> Privacy & Security -> Certificates -> View Certificates -> Authorities tab -> Import -> select static-ca.crt -> Check "Trust this CA to identify websites" -> OK



??? note "Windows"

    Trust the CA using `certutil`

    ```bash
    certutil.exe -addstore root C:\\path\\to\\myCA.pem
    ```

    1. Navigate to the `404/` directory and locate the `../static_proxy/certs/` directory.
    2. Double-click the file labeled `static-ca.crt` (may appear without .crt extension)
    3. Click `Install Certificate...`
    4. Select `Current User` and click `Next`
    5. Choose `Place all certificates in the following store` and click `Browse...`
    6. Select `Trusted Root Certification Authorities` and click `OK`
    7. Click `Next` then `Finish`

??? note "macOS"

    ```bash
    $ sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain static_proxy/certs/static-ca.crt
    ```

    Or use the GUI:

    1. Open Keychain Access
    2. File -> Import Items -> select static-ca.crt
    3. Find the certificate, double-click it
    4. Expand "Trust" and set "When using this certificate" to "Always Trust"


??? note "Linux"

    ```bash
    # Copy CA to system trust store
    $ sudo cp static_proxy/certs/static-ca.crt /usr/local/share/ca-certificates/static-ca.crt
    $ sudo update-ca-certificates
    ```

## Configure your Browser

Set your browser (or system) to use `localhost:8080` (or `127.0.0.1:8080`) as an HTTP/HTTPS proxy.

- **Chrome/Edge:** Settings -> System -> Open your computer's proxy settings
- **Firefox:** Settings -> Network Settings -> Manual proxy configuration -> HTTP Proxy: `127.0.0.1`, Port: `8080`, check "Also use this proxy for HTTPS"

***Important:*** **This tool is a TLS-terminating proxy (man-in-the-middle) and has access to your plaintext HTTPS data (usernames, passwords, certain message protocols, etc.). Do NOT share your CA cert with *anyone* for *anything, ever*.**

*UX on Firefox is slightly more stable for reasons that are not clear to me. Would love some insight. Login flows have been tested and are working in both browsers.*

### Compile & attach eBPF program to TC egress hook (if using Linux)

> The eBPF `ttl_editor` modifies packet-level fingerprints (TTL, TCP window size, sequence numbers, etc.). This requires a Linux kernel.

![tcpdump output](assets/images/tcpdump_output.png)

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

# Notes

---