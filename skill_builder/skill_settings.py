from typing import Optional

from inoft_vocal_framework.dummy_object import dummy_object
from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type, raise_if_variable_not_expected_type_and_not_none
from inoft_vocal_framework.speech_synthesis.polly import VOICES


class Settings:
    class Deployment:
        class Endpoints:
            pass
            """       
             self._endpoints = endpoints
                    "endpoints": {
                        "type": "dict",
                        "schema": {
                            "alexaApiEndpointUrlNotRecommendedToUse": {
                                "type": "string"
                            },
                            "googleAssistantApiEndointUrl": {
                                "type": "string"
                            },
                            "samsungBixbyApiEndointUrl": {
                                "type": "string"
                            },
                            "siriApiEndointUrl": {
                                "type": "string"
                            },
                        }
                    }
                }"""

        def __init__(self, handler_function_path: str, api_gateway_id: str, s3_bucket_name: str, lambda_name: str, endpoints: Endpoints):
            self.handler_function_path = handler_function_path
            self.api_gateway_id = api_gateway_id
            self.s3_bucket_name = s3_bucket_name
            self.lambda_name = lambda_name
            self.endpoints = endpoints

        @property
        def handler_function_path(self) -> str:
            return self._handler_function_path

        @handler_function_path.setter
        def handler_function_path(self, handler_function_path: str) -> None:
            raise_if_variable_not_expected_type(value=handler_function_path, expected_type=str, variable_name="handler_function_path")
            self._handler_function_path = handler_function_path

        @property
        def api_gateway_id(self) -> str:
            return self._api_gateway_id

        @api_gateway_id.setter
        def api_gateway_id(self, api_gateway_id: str) -> None:
            raise_if_variable_not_expected_type(value=api_gateway_id, expected_type=str, variable_name="api_gateway_id")
            self._api_gateway_id = api_gateway_id

        @property
        def s3_bucket_name(self) -> str:
            return self._s3_bucket_name

        @s3_bucket_name.setter
        def s3_bucket_name(self, s3_bucket_name: str) -> None:
            raise_if_variable_not_expected_type(value=s3_bucket_name, expected_type=str, variable_name="s3_bucket_name")
            self._s3_bucket_name = s3_bucket_name

        @property
        def lambda_name(self) -> str:
            return self._lambda_name

        @lambda_name.setter
        def lambda_name(self, lambda_name: str) -> None:
            raise_if_variable_not_expected_type(value=lambda_name, expected_type=str, variable_name="lambda_name")
            self._lambda_name = lambda_name

        @property
        def endpoints(self) -> Endpoints:
            return self._endpoints

        @endpoints.setter
        def endpoints(self, endpoints: Endpoints) -> None:
            raise_if_variable_not_expected_type(value=endpoints, expected_type=self.Endpoints, variable_name="endpoints")
            self._endpoints = endpoints

    def __init__(self, characters_voices: Optional[dict] = None, deployment: Optional[Deployment] = None):
        self.characters_voices = characters_voices
        self.deployment = deployment

    @property
    def characters_voices(self) -> dict:
        return self._characters_voices if self._characters_voices is not None else dummy_object

    @characters_voices.setter
    def characters_voices(self, characters_voices: characters_voices) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=characters_voices, expected_type=dict, variable_name="characters_voices")
        self._characters_voices = characters_voices

    @property
    def deployment(self) -> Deployment:
        return self._deployment if self._deployment is not None else dummy_object

    @deployment.setter
    def deployment(self, deployment: Deployment) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=deployment, expected_type=self.Deployment, variable_name="deployment")
        self._deployment = deployment


def prompt_get_settings(root_folderpath: Optional[str] = None) -> Settings:
    import os

    if root_folderpath is None:
        from inoft_vocal_framework.cli.components import current_project_directory
        root_folderpath = current_project_directory.prompt()

    print("Searching for your app_settings file...")

    found_settings_filepaths = []
    for filename in os.listdir(root_folderpath):
        if filename in ["app_settings.py", "settings.py"]:
            found_settings_filepaths.append(os.path.join(root_folderpath, filename))

    settings_filepath = None
    if len(found_settings_filepaths) == 0:
        raise Exception("Did not found an app_settings.py or settings.py file.\nDid you renamed your settings file ?"
                        "\nOr did you not navigated to the directory of your project ?"
                        "\nTry to run the command cd 'C:/folder/subfolder/myproject'."
                        "\nIf your project is on an external hard-drive (like F:), you must run the cd command, and also the letter name of your hard-drive."
                        "\nSo if your project is in F:/folder/subfolder/myproject, in your command line, run   F:   then run   cd F:/folder/subfolder/myproject")
    elif len(found_settings_filepaths) == 1:
        print(f"Using setting file {found_settings_filepaths[0]}")
        settings_filepath = found_settings_filepaths[0]
    elif len(found_settings_filepaths) > 1:
        while settings_filepath is None:
            print(f"Found {len(found_settings_filepaths)} settings file at following paths :")
            for i_file, file in enumerate(found_settings_filepaths):
                print(f"{i_file + 1} - {file}")

            import click
            file_index = str(click.prompt("What is the number of the file you wish to use ?"))
            if not file_index.isdigit() or int(file_index) > len(found_settings_filepaths) or int(file_index) < 0:
                print("Please write a valid file index in the form of an int like 1 or 3")
            else:
                selected_filepath = found_settings_filepaths[int(file_index) - 1]
                print(f"Selected settings filepath : {click.style(text=selected_filepath, fg='blue')}")
                settings_filepath = selected_filepath


    import importlib.util
    spec = importlib.util.spec_from_file_location("plugin_core", settings_filepath)
    current_plugin_core_module = importlib.util.module_from_spec(spec=spec)
    spec.loader.exec_module(current_plugin_core_module)

    vars_current_settings_module = vars(current_plugin_core_module)
    if "settings" not in vars_current_settings_module.keys():
        raise Exception(f"The variable named 'settings' is missing from the settings file you selected at {settings_filepath}")
    else:
        settings_instance = vars_current_settings_module["settings"]
        if isinstance(settings_instance, Settings):
            return settings_instance
        else:
            raise Exception(f"A variable named settings has been found in the file {settings_instance}, but it was not an instance of Settings type.")
    # This code line is unreachable, no need for an additional exception


if __name__ == "__main__":
    Settings(characters_voices={
        "Léo": VOICES.French_France_Male_MATHIEU,
        "Willie": VOICES.French_France_Female_CELINE,
        "Luc": VOICES.Russian_Russia_Male_MAXIM,
        "Menu": VOICES.Icelandic_Iceland_Male_KARL,
        "default": VOICES.French_France_Female_CELINE
    })
