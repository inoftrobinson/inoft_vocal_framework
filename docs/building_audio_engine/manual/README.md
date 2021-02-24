## Building on and for Windows :

**This must imperatively be run on a Windows computer or virtual machine**

*For requirements, see the README file of the 'building_audio_engine' folder.*


#### Navigate to the root audio_engine folder

`cd .../inoft_vocal_framework/audio_engine/`

#### Run the cargo build 

`cargo build --release --features $python-version`

Where $python-version can be :

- python39
- python38

An `audio_file.dll` file will be generated in `.../inoft_vocal_framework/audio_engine/target/release` folder. Copy it to `.../inoft_vocal_framework/audio_engine` and rename the file from `audio_engine.dll` to `audio_engine.pyd`, which will allows Python to read the file.



## Consuming :

### AWS Lambda :

AWS Lambda runs on Linux. If you try to use a version of the framework that has been build for Windows, but not for Linux, you will get the error `Module not found`, because when running the `import audio_engine` line in Python running on Linux, it will not look for `audio_engine.pyd` like it would on Windows, but it will look for `audio_engine.so`

Please follow the instructions on how to build on Linux. 



---



## Building on and for Linux :

**This must imperatively be run on a Linux computer or virtual machine**

For requirements, see the README file of the 'building_audio_engine' folder.

#### Navigate to the root audio_engine folder

`cd .../inoft_vocal_framework/audio_engine/`

#### Run the cargo build 

`cargo build --release --features $python-version`

Where $python-version can be :

- python39
- python38

#### Rename the build file : 

Navigate into the release folder

`cd target/release` 

The generated file will be called libaudio_engine.so, rename it to audio_engine.so (the other generated files are cache or infos files that can be discarded)

`cp libaudio_engine.so audio_engine.so` 

If you do not do this step, you would  get an `ImportError: dynamic module does not define module export function (PyInit_libaudio_engine)` where the expected module name defined in the code (audio_engine) was not matching the name of the file.

#### Packing the linked libraries

If missing, create the 'libs' folder `.../inoft_vocal_framework/audio_engine/libs`

Go to `/usr/lib/x86_64-linux-gnu` and copy/rename inside the 'libs' folder folder the following files : 

- `libssl.so.1.1` -> `libssl.so.1.1`
- `libcrypto.so.1.1` -> `libcrypto.so.1.1`
- `libmp3lame.so.0.0.0` -> `libmp3lame.so.0` (need to be renamed, because the file that is searched, is actually a symbolic link)
- `libm-2.31.so` -> `lib64/libm.so.6`

It shoud look like this : 

![](assets/LinuxLibsFolderContent.PNG)






