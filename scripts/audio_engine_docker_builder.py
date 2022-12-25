import os
import subprocess

python_version = "3.8"

inoft_vocal_framework_root_dirpath: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
print(f"Using '{inoft_vocal_framework_root_dirpath}' as inoft_vocal_framework root dirpath")

build_command: str = (
    f'docker run --mount type=bind,source={inoft_vocal_framework_root_dirpath},target=/inoft_vocal_framework '
    f'be41f6d42ce628ee2466f704501484be680991fa34fc8c028c74f51275c3d1d7 '
    f'python /inoft_vocal_framework/scripts/audio_engine_build_cli.py '
    f'--python_version python38 '
    f'--os_key linux '
)
subprocess.run(build_command)