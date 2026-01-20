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

<details>
<summary><b>Windows install</b></summary>

<h2> Option 1: Install via winget (recommended) </h2>

<h3> 1. Open the Command Prompt </h3>

<p>
- Press... Windows button + r
</p>

<p>
- Type "cmd" into the run dialogue box.
</p>

<h3> 2. Download the dependencies </h3>

```bash
$ winget install Kitware.CMake
$ winget install nasm -i
```

<sub> Restart your shell after installation. Tools should be on your PATH automatically. </sub>
</details>

<details>
<summary><b>macOS install</b></summary>

<h2> Install via homebrew (recommended) </h2>

<ol>
<li> Open the Terminal </li>

<li> Download dependencies w/ homebrew: </li>

<ul>
<li><code> $ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" </code></li>

<li><code> $ brew install rust nasm cmake </code></li>
</ul>

<sub>Restart your shell after installation. Tools should be on your PATH automatically.</sub>
</ol>
</details>

<details>
<summary><b>Linux install</b></summary>

<h2>Install via package manager</h2>

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