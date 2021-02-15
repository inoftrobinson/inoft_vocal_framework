### Pre-requisites :

Make sure that the libs folder exist in the virtual environment of the project.
If its not the case, go to the installation folder of the used Python version,
copy the libs folder
![](./images/python_libs_folder.PNG)

_The folder should contain 'lib' files, like so for a Python 3.9 installation._

![](./images/python_libs_folder_content.PNG)

Paste the libs folder to the venv of the project used to work on the 
inoft_vocal_engine or inoft_vocal_framework. It should look like this.
![](./images/python_libs_folder_in_venv.PNG)

---

### Building on Windows :
cd in the rust cargo project root folder, and run `cargo build --release`

![](./images/run_cargo_build_release.PNG)

Navigate into the build folder, find the .dll file of the build 
(for example 'inoft_audio_engine_rendered.dll').
![](./images/dll_file_of_release_build.PNG)
 
Copy the file to the root folder of the project used to work on the 
inoft_vocal_engine or inoft_vocal_framework.
![](./images/pasted_dll_file_in_root_project_folder.PNG)

Rename the file extension of the file from .dll to .pyd
![](./images/renaming_dll_to_pyd.PNG) 
->
![](./images/renamed_dll_to_pyd.PNG)


The dll will now be able to be imported as a standard python library. 

For example :
![](./images/use_in_python_console.PNG)

_Each time the rust code is modified, all of theses steps (new build, and 
setting up the Python module) needs to be repeated. Have fun ! :)_

