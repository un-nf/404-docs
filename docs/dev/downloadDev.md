---
title: Working with the 404 Repository
description: Download or clone the 404 anti-fingerprinting proxy repository. Get the latest version from GitHub and set up your local development environment.
hide:
  - toc
---

# Getting Started - Download 404

## Download (easy)

The *simplest* option is to download a zipped version of the repository. *This does not guarantee an up-to-date version of the application*.

1. [**Download .zip**](../assets/404.zip)

    !!! Warning ".zip file last updated: 2/11/2026"

    Please be sure to move this .zip file to the location you would like it (e.g. `~/git/`) before unzipping the file. Though moving the repo is a simple enough process at any time, doing so now will save you from losing it in your `Downloads/` folder as well as allow you to use the commands provided more seamlessly.

2. Create a new directory @ `~/git/` to house `404`

!!! Success "You may skip this step if you already have a `git/` or `projects/` directory."

You can do this using the following commands...

**Windows**: 

Open the Command Prompt

- Press... :material-microsoft-windows: + r

- Type "cmd" into the run dialogue box.

```bash
if not exist "%USERPROFILE%\git" mkdir "%USERPROFILE%\git"
move "%USERPROFILE%\Downloads\404.zip" "%USERPROFILE%\git\404.zip"
tar -xf "%USERPROFILE%\git\404.zip" -C "%USERPROFILE%\git"
del "%USERPROFILE%\git\404.zip"

```

**Linux/macOS**: 

Open the Terminal

- Press :material-apple-keyboard-command: + space
- Search "Terminal" and press Enter

```zsh
mkdir -p "$HOME/git"
mv "$HOME/Downloads/404.zip" "$HOME/git/404.zip"
unzip "$HOME/git/404.zip" -d "$HOME/git"
rm "$HOME/git/404.zip"

```

**OR** by using the *file explorer*.

Place the .zip file in `~/git/` and right-click on it to extract a new directory: `~/git/404`.

## Clone (secure)

The *best* option is to use your command line to download the latest version of the repository from `Github` or `Codeberg`.

**1. Create a folder for 404** *or navigate to your `git` directory.*

Windows:
```
mkdir -p %USERPROFILE%\git\
cd %USERPROFILE%\git\
```

Linux/macOS:
```
mkdir -p ~/git/
cd ~/git/
```

**2. Clone to your local projects/ or git/ directory**

All operating systems: 
```
git clone https://github.com/un-nf/404.git
cd 404
```

??? question "Windows clone"

    Use Command Prompt to clone the repository from GitHub.

    1. Open Command Prompt

        - Press... :material-microsoft-windows: + r
        - Type "cmd" into the run dialogue box and press Enter

    2. Create (if needed) and enter your `git` directory

    ```cmd
    if not exist "%USERPROFILE%\git" mkdir "%USERPROFILE%\git"
    cd /d "%USERPROFILE%\git"

    ```

    3. Clone and enter the project folder

    ```cmd
    git clone https://github.com/un-nf/404.git
    cd 404

    ```

    If `git` is not installed, install Git for Windows from https://git-scm.com/downloads/win and rerun the commands.


??? question "macOS clone"

    Use Terminal to clone the repository from GitHub.

    1. Open Terminal

        - Press :material-apple-keyboard-command: + space
        - Search "Terminal" and press Enter

    2. Verify that Git is installed

    ```zsh
    git --version

    ```

    If you see "command not found", install Apple Command Line Tools:

    ```zsh
    xcode-select --install

    ```

    3. Create (if needed) and enter your `git` directory

    ```zsh
    mkdir -p "$HOME/git"
    cd "$HOME/git"

    ```

    4. Clone and enter the project folder

    ```zsh
    git clone https://github.com/un-nf/404.git
    cd 404

    ```

[Step 2 - Download Dependencies](./depsDev.md){.md-button .md-button--primary}