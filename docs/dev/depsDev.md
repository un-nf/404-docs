# Getting Started with the Repository

## Requirements

*Utilizing the eBPF module requires a Linux kernel (4.15+).*

| Component | Version | Install Link |
|-----------|---------|-------|
| **Rust** | 1.76+ | [INSTALL](https://rust-lang.org/tools/install/) - *manual install req.* |
| **CMake** | Latest | [INSTALL](https://www.nasm.us/pub/nasm/releasebuilds/3.01/) |
| **NASM** | Latest | [INSTALL](https://cmake.org/download/) |

> *You may install these manually, but it is often easier to install them via `brew` or `winget`. So open the Terminal and lets get started!*

## Install dependencies & configure PATH

??? note "Windows install"
    
    Option 1: Install via winget (recommended) 

    1. Open the Command Prompt
    
        - Press... Windows button + r

        - Type "cmd" into the run dialogue box.


    2. Download the dependencies

    ```bash
    winget install Kitware.CMake\ 
    winget install nasm -i
    ```

    Restart your shell after installation. Tools should be on your PATH automatically. 


??? note "macOS install"
    Install via homebrew (recommended) 

    Open the Terminal

    Download dependencies w/ homebrew:

    ```zsh
    brew install rust nasm cmake
    ```

    Restart your shell after installation. Tools should be on your PATH automatically.

??? note "Linux install"

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
