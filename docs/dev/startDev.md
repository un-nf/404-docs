---
title: Working with the 404 Repository
description: Run the 404 STATIC proxy, trust the locally-generated CA certificate, and configure your browser to route traffic through localhost:8080.
hide:
  - toc
---

# Getting Started

[Step 2 - Download Dependencies](./depsDev.md){.md-button .md-button--primary}

!!! Info "All steps assume that there is a folder named `404/` located at `~/git/`"

## Run the proxy

!!! Tip "All commands can be copy pasted into your terminal for easy usage!"

Linux/macOS:

```bash
cd ~/git/404/src/STATIC_proxy # CHANGE to wherever you unzipped the 404 folder.
cargo run  # This will take a while on the first run (~5-minutes)
```

Windows:

```bash
cd %USERPROFILE%\git\404\src\STATIC_proxy # CHANGE to wherever you unzipped the 404 folder.
cargo run  # This will take a while on the first run (~5-minutes)
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
    ***or*** manually...
    1. Navigate to the `404/` directory and locate the `../static_proxy/certs/` directory.
    2. Double-click the file labeled `static-ca.crt` (may appear without .crt extension)
    3. Click `Install Certificate...`
    4. Select `Current User` and click `Next`
    5. Choose `Place all certificates in the following store` and click `Browse...`
    6. Select `Trusted Root Certification Authorities` and click `OK`
    7. Click `Next` then `Finish`

??? note "macOS"

    ```zsh
    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain static_proxy/certs/static-ca.crt
    ```

    Or use the GUI:

    1. Open Keychain Access
    2. File -> Import Items -> select static-ca.crt
    3. Find the certificate, double-click it
    4. Expand "Trust" and set "When using this certificate" to "Always Trust"


??? note "Linux"

    ```bash
    # Copy CA to system trust store
    sudo cp static_proxy/certs/static-ca.crt /usr/local/share/ca-certificates/static-ca.crt
    sudo update-ca-certificates
    ```

## Configure your Browser

Set your browser (or system) to use `localhost:8080` (or `127.0.0.1:8080`) as an HTTP/HTTPS proxy.

- **Chrome/Edge:** Settings -> System -> Open your computer's proxy settings
- **Firefox:** Settings -> Network Settings -> Manual proxy configuration -> HTTP Proxy: `127.0.0.1`, Port: `8080`, check "Also use this proxy for HTTPS"

***Important:*** **This tool is a TLS-terminating proxy (man-in-the-middle) and has access to your plaintext HTTPS data (usernames, passwords, certain message protocols, etc.). Do NOT share your CA cert with *anyone* for *anything, ever*.**

*UX on Firefox is slightly more stable for reasons that are not clear to me. Would love some insight. Login flows have been tested and are working in both browsers.*

## *Optional* - Configure a Linux VM (if not using Linux)

**VM Setup:**

> *VM images coming soon. I am using an Alpine distribution on WSL2 (Windows). Works well, but a little heavy. Definitely going to be looking into distributing the VMs as dedicated server images, not gerry-rigged forwarding machines with desktop environments.*

You *100% could* configure a VM and route traffic from your host machine to a VM guest, [instructions for VM configuration here](ebpf.md).

For now, just running STATIC should be enough, though network level obfuscation is not possible without a Linux kernel (yet).

[Step 4 *(optional)* - Setup eBPF](./ebpf.md){.md-button .md-button--primary}