import os
from typing import Optional, Dict, Any

import click
import platform
import shutil
import subprocess
from pathlib import Path


@click.command()
@click.option(
    "-pyv", "--python_version", type=click.Choice(['python38', 'python39']), prompt="Python version to compile to",
    help="The python version to compile to. Available choices : 'python38', 'python39'"
)
@click.option(
    "-os", "--os_key", type=click.Choice(['windows', 'linux']), prompt="OS to compile to",
    help="The OS to compile to. Available choices : 'windows', 'linux'. Must be ran on the matching OS."
)
def build(os_key: str, python_version: str):
    active_platform = platform.system()
    # build_target: str = "x86_64-unknown-linux-musl"
    build_target = None

    if os_key == 'windows':
        if active_platform != "Windows":
            raise Exception(f"To compile for Windows, please run this script on a Windows computer or virtual machine (tested with Windows 10)")
        build_windows(python_version=python_version, target=build_target)
    elif os_key == 'linux':
        if active_platform != "Linux":
            raise Exception(f"To compile for Linux, please run this script on a Linux computer or virtual machine (tested with Ubuntu desktop)")
        build_linux(python_version=python_version, target=build_target)
    else:
        raise Exception(f"OS {os_key} not supported")

def _construct_cargo_build_command(value_args: Dict[str, Optional[Any]]) -> str:
    value_args_statement: str = " ".join([
        f"--{key} {value}"
        for key, value in value_args.items()
        if value is not None
    ])
    build_command: str = f"cargo build --release {value_args_statement}"
    return build_command


def build_windows(python_version: str, target: Optional[str]):
    audio_engine_dirpath = os.path.join(Path(os.path.dirname(os.path.realpath(__file__))).parent, "audio_engine")
    os.chdir(audio_engine_dirpath)

    audio_engine_dll_relative_filepath = "target/release/audio_engine.dll"
    audio_engine_dll_absolute_filepath = os.path.join(audio_engine_dirpath, audio_engine_dll_relative_filepath)
    if os.path.isfile(audio_engine_dll_relative_filepath):
        os.remove(audio_engine_dll_relative_filepath)
        click.echo(f"Removed existing dll file at {audio_engine_dll_absolute_filepath}")

    cargo_build_command: str = _construct_cargo_build_command(
        value_args={'target': target, 'features': python_version}
    )
    compilation_result = subprocess.run(cargo_build_command, shell=True)
    if not os.path.isfile(audio_engine_dll_relative_filepath):
        raise Exception(f"No file found at {audio_engine_dll_absolute_filepath} after compilation. The compilation must have encountered a problem.")

    audio_engine_pyd_relative_filepath = "audio_engine.pyd"
    audio_engine_pyd_absolute_filepath = os.path.join(audio_engine_dirpath, audio_engine_pyd_relative_filepath)
    if os.path.isfile(audio_engine_pyd_relative_filepath):
        os.remove(audio_engine_pyd_relative_filepath)
        click.echo(f"Removed existing pyd file at {audio_engine_pyd_absolute_filepath}")

    shutil.copyfile(audio_engine_dll_relative_filepath, audio_engine_pyd_relative_filepath)
    click.echo(f"Finished copy of dll file from {audio_engine_dll_absolute_filepath} to {audio_engine_pyd_absolute_filepath}")

def build_linux(python_version: str, target: Optional[str]):
    audio_engine_dirpath = os.path.join(Path(os.path.dirname(os.path.realpath(__file__))).parent, "audio_engine")
    os.chdir(audio_engine_dirpath)

    audio_engine_lib_relative_filepath = "target/release/libaudio_engine.so"
    audio_engine_lib_absolute_filepath = os.path.join(audio_engine_dirpath, audio_engine_lib_relative_filepath)
    if os.path.isfile(audio_engine_lib_relative_filepath):
        os.remove(audio_engine_lib_relative_filepath)
        click.echo(f"Removed existing lib file at {audio_engine_lib_absolute_filepath}")

    cargo_build_command: str = _construct_cargo_build_command(
        value_args={'target': target, 'features': python_version}
    )
    compilation_result = subprocess.run(cargo_build_command, shell=True)
    if not os.path.isfile(audio_engine_lib_relative_filepath):
        raise Exception(f"No file found at {audio_engine_lib_absolute_filepath} after compilation. The compilation must have encountered a problem.")

    audio_engine_so_relative_filepath = "audio_engine.so"
    audio_engine_so_absolute_filepath = os.path.join(audio_engine_dirpath, audio_engine_so_relative_filepath)
    if os.path.isfile(audio_engine_so_relative_filepath):
        os.remove(audio_engine_so_relative_filepath)
        click.echo(f"Removed existing so file at {audio_engine_so_absolute_filepath}")

    shutil.copyfile(audio_engine_lib_relative_filepath, audio_engine_so_relative_filepath)
    click.echo(f"Finished copy of dll file from {audio_engine_lib_absolute_filepath} to {audio_engine_so_absolute_filepath}")


if __name__ == '__main__':
    build()

