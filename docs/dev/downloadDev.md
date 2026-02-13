# Getting Started - Download 404

### Download (easy)

The *simplest* option is to download a zipped version of the repository. *This does not guarantee an up-to-date version of the application*.

1. [**Download .zip**](../assets/404.zip)

!!! Warning ".zip file last updated: 2/11/2026"

Please be sure to move this .zip file to the location you would like it (e.g. `~/git/`) before unzipping the file. Though moving the repo is a simple enough process at any time, doing so now will save you from losing it in your `Downloads/` folder as well as allow you to use the commands provided more seamlessly.

2. Create a new directory @ `~/git/` to house `404`

!!! Note "You may skip this step if you already have a `git/` or `projects/` directory."

You can do this using the following commands...

**Windows**: 

Open the Command Prompt

    - Press... :material-microsoft-windows: + r

    - Type "cmd" into the run dialogue box.

```bash
mkdir "%USERPROFILE%\git" ^
&& move "%USERPROFILE%\Downloads\404.zip" "%USERPROFILE%\git" ^
&& tar -xf "%USERPROFILE%\git\404.zip" -C "%USERPROFILE%\git" ^
&& del "%USERPROFILE%\git\404.zip"
```

**Linux/macOS**: 

Open the Terminal

    - Press :material-apple-keyboard-command: + space
    - Search "Terminal" and press Enter

```zsh
mkdir -p "$HOME/git" \
&& mv "$HOME/Downloads/404.zip" "$HOME/git" \
&& unzip "$HOME/git/404.zip" -d "$HOME/git" \
&& rm "$HOME/git/404.zip"
```

**OR** by using the *file explorer*.

Place the .zip file here and click on it to extract a new directory: `~/git/404` automatically.

### Clone (secure)

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

??? note "Windows install"
    
    Install via winget

    1. Click [here](https://static.rust-lang.org/rustup/dist/i686-pc-windows-msvc/rustup-init.exe) (32-bit) to download rust-up. Open the downloaded `.exe` file and follow setup instructions.

        - Use the “Workload” tab to select the “Desktop Development with C++” option.
        - [Help](https://rust-lang.github.io/rustup/installation/windows-msvc.html)

    2. Open the Command Prompt
    
        - Press... :material-microsoft-windows: + r

        - Type "cmd" into the run dialogue box.


    3. Download the dependencies

    ```bash
    winget install --id Kitware.CMake -e && winget install --id NASM.NASM -e
    ```

    Restart your shell after installation. Tools should be on your PATH automatically. 


??? note "macOS install"
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

    2. Download dependencies w/ homebrew:

    ```zsh
    brew install rust nasm cmake
    ```

    Restart your shell after installation. Tools should be on your PATH automatically.
