---
title: Working with the 404 Repository
description: Step-by-step guide to installing Rust, CMake, and NASM dependencies for building 404's anti-fingerprinting proxy on Windows, macOS, and Linux.
hide:
  - toc
---

# Getting Started with the Repository

[Step 1 - Download 404](./downloadDev.md){.md-button .md-button--primary}

## Requirements

*Utilizing the eBPF module requires a Linux kernel (4.15+).*

| Component | Version | Install Link |
|-----------|---------|-------|
| **Rust** | 1.76+ | [INSTALL](https://rust-lang.org/tools/install/){target="_blank"} |
| **CMake** | Latest | [INSTALL](https://cmake.org/download/){target="_blank"} |
| **NASM** | Latest | [INSTALL](https://www.nasm.us/pub/nasm/releasebuilds/3.01/){target="_blank"} |

> *You may install these manually, but it is often easier to install them via `brew` or `winget`. So open the Terminal and lets get started!*

## Install dependencies & configure PATH

!!! tip "All commands can be copy pasted into your terminal for easy usage!"

=== "Windows"
    
    Install via winget

    1. Click [here](https://static.rust-lang.org/rustup/dist/i686-pc-windows-msvc/rustup-init.exe) (32-bit) to download rust-up. Open the downloaded `.exe` file and follow setup instructions.

        - Use the “Workload” tab to select the “Desktop Development with C++” option.
        - [Help](https://rust-lang.github.io/rustup/installation/windows-msvc.html){target="_blank"}

    2. Open the Command Prompt
    
        - Press... :material-microsoft-windows: + r

        - Type "cmd" into the run dialogue box.


    3. Download the dependencies

    ```bash
    winget install --id Kitware.CMake -e && winget install --id NASM.NASM -e
    ```

    Restart your shell after installation. Tools should be on your PATH automatically. 


=== "macOS"

    Install via homebrew (recommended) 

    1. Open the Terminal

        - Press :material-apple-keyboard-command: + space
        - Search "Terminal" and press Enter

    2. Ensure you have homebrew installed

        a.
        ```zsh
        xcode-select --install 
        ```

        b.
        ```zsh
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```

    3. Download dependencies w/ homebrew:

    ```zsh
    brew install rust nasm cmake
    ```

    Restart your shell after installation. Tools should be on your PATH automatically.

=== "Linux"

    Install via package manager

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

[Step 3 - Start Proxy](./startDev.md){.md-button .md-button--primary}