import os
import string
import boto3
import click
from pathlib import Path
from random import choice
import inoft_vocal_framework
from inoft_vocal_framework.cli.aws_utils import is_valid_bucket_name, BUCKET_NAMING_MSG


BOTO3_CONFIG_DOCS_URL = "https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration"

def _get_from_name_or_ask_to_select_template(selected_template_name: str = None) -> dict:
    current_folder_path = Path(os.path.dirname(os.path.abspath(__file__)))
    templates_folder_path = os.path.join(current_folder_path.parent, "templates")
    invalid_folder_names = ["__pycache__"]

    available_templates = dict()
    for template_dir_name in os.listdir(templates_folder_path):
        if template_dir_name not in invalid_folder_names:
            if os.path.isdir(os.path.join(templates_folder_path, template_dir_name)):
                current_template_dir_path = os.path.join(templates_folder_path, template_dir_name)
                files_names_in_current_template_dir = os.listdir(current_template_dir_path)

                if not len(files_names_in_current_template_dir) > 0:
                    print(f"That's strange. The template folder at {current_template_dir_path} "
                          f"did not contain any file, and so cannot be used.")
                else:
                    paths_to_files_to_copy = list()
                    for filename in files_names_in_current_template_dir:
                        if filename not in ["infos.yaml", "infos.json"]:
                            filepath = os.path.join(current_template_dir_path, filename)
                            if os.path.isfile(filepath):
                                paths_to_files_to_copy.append(filepath)

                    if not len(paths_to_files_to_copy) > 0:
                        print(f"That's strange. The template folder at {current_template_dir_path} "
                              f"did not contain any file that could be copied, and so cannot be used.")
                    else:
                        current_template_infos_dict = None

                        if "infos.yaml" in files_names_in_current_template_dir:
                            from inoft_vocal_framework.utils.general import load_yaml
                            current_template_infos_dict = load_yaml(filepath=os.path.join(current_template_dir_path, "infos.yaml"))
                        elif "infos.json" in files_names_in_current_template_dir:
                            from inoft_vocal_framework.utils.general import load_json
                            current_template_infos_dict = load_json(filepath=os.path.join(current_template_dir_path, "infos.json"))

                        if isinstance(current_template_infos_dict, dict):
                            if "name" in current_template_infos_dict.keys() and isinstance(current_template_infos_dict["name"], str):
                                available_templates[current_template_infos_dict["name"]] = {"pathsToFilesToCopy": paths_to_files_to_copy}
                                continue

                        available_templates[template_dir_name] = {"pathsToFilesToCopy": paths_to_files_to_copy}
                        # If the no infos dict has been created or that no name variable has been found in the infos, we will not have
                        # triggered the continue keyword, and so we will reach this stage where we add the template with its folder name.

    if selected_template_name is None:
        selected_template_name = click.prompt("Type the name of the template you would like to use, the followings are available :",
                                              type=click.Choice(available_templates.keys()))
        # todo: improve that, i would like for the user to select it with a list select (like in PyInquirer)

    if selected_template_name in available_templates.keys():
        return available_templates[selected_template_name]
    else:
        return None

def new(template_name: str = None, project_folderpath: str = None):
    current_folder_path = Path(os.path.dirname(os.path.abspath(__file__)))
    selected_template_dict = _get_from_name_or_ask_to_select_template(selected_template_name=template_name)
    selected_templates_files_to_copy = selected_template_dict["pathsToFilesToCopy"]

    if project_folderpath is None:
        while True:
            project_folderpath = click.prompt(text="To which folder location would like to put the template ?",
                                              default=Path(os.path.dirname(os.path.realpath(inoft_vocal_framework.__file__))).parent)
            if not os.path.isdir(project_folderpath):
                print(f"No folder has been found at {click.style(text=project_folderpath, bold=True, fg='blue')}."
                      f"\nPlease write a valid folder path, or exit the CLI by using CTRL+C")
            else:
                break

            """if click.confirm("You now need to select a folder where your project (and your template) will be located. Type y"):
                from inoft_vocal_framework.cli.gui_handlers import select_folder
                project_folderpath = select_folder(title="Folder for your project", initial_dir=current_folder_path.parents[1])
                break
                # todo: find a way to make the gui works (right now, it just freeze the script and the folderpicker window never opens)
            else:
                if click.confirm("Do you want to select a different template ?"):
                    selected_template_dict = _get_from_name_or_ask_to_select_template()
                    selected_templates_files_to_copy = selected_template_dict["pathsToFilesToCopy"]
                else:
                    print("We do not know how to help you."
                          "\nIf you have questions on how the framework works, please visit or GitHub page : " +
                          click.style("https://github.com/Robinson04/inoft_vocal_framework", fg="cyan", bold=True))"""

    Path(project_folderpath).mkdir(exist_ok=True)

    for src_file_path in selected_templates_files_to_copy:
        from shutil import copy
        destination_filepath = os.path.join(project_folderpath, Path(src_file_path).name)
        if os.path.isfile(destination_filepath):
            if click.confirm(f"A file already exist at {destination_filepath}. Do you wish to keep the existing file and not replace it ?"):
                continue
        click.echo(f"Copying {src_file_path} to {destination_filepath}")
        copy(src_file_path, destination_filepath)
    click.echo("Template copying completed.")

    """
    # Detect AWS profiles and regions
    session = boto3.session.Session()
    profile_names = session.available_profiles

    click.echo("\nAWS Lambda and API Gateway are only available in certain regions. "
               "Let's check to make sure you have a profile set up in one that will work.")

    if not profile_names:
        click.echo(f"We couldn't find an AWS profile to use. Before using the Inoft Vocal Framework, you'll need to set one up."
                   f"\nSee here for more info: {click.style(BOTO3_CONFIG_DOCS_URL, fg='blue', underline=True)}")
        return None
    elif len(profile_names) == 1:
        used_profile_name = profile_names[0]
        click.echo(f"Okay, using profile '{click.style(used_profile_name, bold=True)}' !")
    else:
        used_profile_name = click.prompt(f"We found the following profiles type the one you would like to use", type=click.Choice(profile_names))

    # Create Bucket
    click.echo("\nYour skills deployments will need to be uploaded to a " + click.style("private S3 bucket", bold=True) + ".")
    click.echo("If you don't have a bucket yet, we'll create one for you too.")
    default_bucket_name = f"inoftskill-{''.join(choice(string.ascii_lowercase + string.digits) for _ in range(9))}"

    bucket_name = click.prompt("What is/will be the name of your bucket ? Default :", default=default_bucket_name)
    while True:
        bucket_name = click.prompt("What is/will be the name of your bucket ? Default :", default=default_bucket_name)

        if is_valid_bucket_name(bucket_name):
            break

        click.echo(click.style("Invalid bucket name!", bold=True))
        click.echo("S3 buckets must be named according to the following rules:")
        click.echo(BUCKET_NAMING_MSG)

    # todo: add multi-regions deployement

    # The given environment name
    zappa_settings = {
        env: {
            'profile_name': profile_name,
            's3_bucket': bucket,
            'runtime': get_venv_from_python_version(),
            'project_name': self.get_project_name()
        }
    }

    if profile_region:
        zappa_settings[env]['aws_region'] = profile_region


    import json as json # json is fine for loading, not fine for writing.
    zappa_settings_json = json.dumps(zappa_settings, sort_keys=True, indent=4)

    click.echo("\nOkay, here's your " + click.style("zappa_settings.json", bold=True) + ":\n")
    click.echo(click.style(zappa_settings_json, fg="yellow", bold=False))

    confirm = input("\nDoes this look " + click.style("okay", bold=True, fg="green")  + "? (default 'y') [y/n]: ") or 'yes'
    if confirm[0] not in ['y', 'Y', 'yes', 'YES']:
        click.echo("" + click.style("Sorry", bold=True, fg='red') + " to hear that! Please init again.")
        return

    # Write
    with open("zappa_settings.json", "w") as zappa_settings_file:
        zappa_settings_file.write(zappa_settings_json)
    """

    click.echo("\nPour en savoir plus sur le framework, rendez-vous sur notre page " + click.style("GitHub", bold=True) +
               " ici : " + click.style("https://github.com/Robinson04/inoft_vocal_framework", fg="cyan", bold=True))
    click.echo("\nExcellente journée ! ;)")
    click.echo(" ~ " + click.style("Robinson Labourdette d'Inoft", bold=True) + "!")

    return

