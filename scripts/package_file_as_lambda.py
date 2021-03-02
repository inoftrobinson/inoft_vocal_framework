import os
from pathlib import Path
from typing import List, Tuple
import click
from tqdm import tqdm

root_path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
framework_root_path = os.path.join(root_path, "inoft_vocal_framework")

folders_names_to_excludes = ["__pycache__", ".idea", ".git", "dist", "speech_synthesis", "temp", "tmp", "target", "build_lame", "src", "DOC_BUILD_CARGO"]
files_extensions_to_exclude = [".wav", ".mp3"]

@click.command()
@click.option("-bfn", "--build_filename", type=str, prompt="Build filename")
@click.option("-llf", "--lambda_layer_filepath", type=click.Path(exists=True), prompt="Your single lambda_layer root filepath")
def package(build_filename: str, lambda_layer_filepath: str):
    output_zip_filepath = os.path.join(root_path, f"{build_filename}.zip")
    if os.path.isfile(output_zip_filepath):
        os.remove(output_zip_filepath)

    if not os.path.isfile(output_zip_filepath):
        files_to_zip: List[Tuple[str, str]] = [(lambda_layer_filepath, "lambda_function.py")]

        # Include the framework files to the archive
        click.echo("Searching framework files to zip...")
        for root_dirpath, dirs, filenames in os.walk(framework_root_path, topdown=True):
            # The topdown arg allow use modify the dirs list in the walk, and so we can easily exclude folders.
            dirs[:] = [dirpath for dirpath in dirs if Path(dirpath).name not in folders_names_to_excludes]
            relative_root_dirpath = os.path.join("inoft_vocal_framework", root_dirpath.replace(framework_root_path, "").strip("\\").strip("/"))
            for filename in filenames:
                if Path(filename).suffix not in files_extensions_to_exclude:
                    files_to_zip.append((os.path.join(root_dirpath, filename), os.path.join(relative_root_dirpath, filename)))

        import zipfile
        with zipfile.ZipFile(output_zip_filepath, "w") as zip_object:
            click.echo("Zipping files...")
            num_files_to_zip = len(files_to_zip)
            for i in tqdm(range(num_files_to_zip)):
                current_file_data = files_to_zip[i]
                zip_object.write(filename=current_file_data[0], arcname=current_file_data[1])

        click.echo(f"Packaged zipped file available at {output_zip_filepath}")


if __name__ == '__main__':
    package()
