## Building on and for Windows :

*Tested and working on Windows 10*

### Pre-requirements :

#### Installations :

Install Rust according to instructions (will auto-detect and give matching instructions according to the operating system) : https://www.rust-lang.org/tools/install

#### Building Lame :

todo


## Building on and for Linux :

*Tested and working on :*

- *Ubuntu 20.04.2 desktop amd64 in a virtual linux machine running in VirtualBox 5.2.12 :*
  - *Ubuntu download : https://ubuntu.com/download/desktop/thank-you?version=20.04.2&architecture=amd64*
  - *VirtualBox download : http://download.virtualbox.org/virtualbox/5.2.12*

### Pre-requirements : 

#### Installations :

Install Rust according to instructions (will auto-detect and give matching instructions according to the operating system) : https://www.rust-lang.org/tools/install

Install the C++ toolchain : `sudo apt install build-essential`

Install openssl : `sudo apt-get install openssl libssl-dev`

Install Lame : `sudo apt-get install libmp3lame0 libmp3lame-dev`

Install Python libraries : `sudo apt-get install libpython3.8 libpython3.8-dev`

#### Cargo :

Make sure cargo is configured to create a C-compatible dynamicly library (where depencies will not included in the final lib file), because Python cannot import static librairies. In the Cargo.toml file, you should have : 

```toml
[lib]
name = "audio_engine"
crate-type = ["cdylib"]
```

#### Python :

Make sure that the default Python version is a Python 3 version when typing python (if python command does not exist, we revert to python3 command)

#### Building Lame:

If missing, build lame
