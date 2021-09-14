from typing import Optional, Union, Dict

import click

from inoft_vocal_framework.dummy_object import dummy_object
from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type_and_not_none
from inoft_vocal_framework.skill_settings.settings_components.deployment import Deployment
from inoft_vocal_framework.skill_settings.settings_components.dynamodb_databases import DatabaseSessionsUsersData, \
    DatabaseMessagesContent, DatabaseUsersNotificationsSubscriptions
from inoft_vocal_framework.skill_settings.settings_components.plugins import Plugins
# from inoft_vocal_engine.speech_synthesis.polly import VOICES
# todo: currently, the voices setting is deprecated since the split between the inoft_vocal_framework and the inoft_vocal_engine
from inoft_vocal_framework.user_data_plugins.base_plugin import UserDataBasePlugin


def prompt_database_warning_message(variable_name: str, instance_type: type):
    click.echo(click.style(
        f"\nWarning ! The variable {variable_name} for the {instance_type.__name__} instance was not properly set.\n"
        f"If you do not need this database client, please set the disable_database variable to True on this instance.",
        fg='yellow'
    ))


class Settings:
    INFRASTRUCTURE_ENGINE = 'engine'
    INFRASTRUCTURE_NEXT_ENGINE = 'next-engine'
    INFRASTRUCTURE_LOCAL_ENGINE = 'local-engine'
    INFRASTRUCTURE_PROVIDED_AWS = 'provided-aws'
    _INFRASTRUCTURE_TYPES_UNION = Union[INFRASTRUCTURE_ENGINE, INFRASTRUCTURE_NEXT_ENGINE, INFRASTRUCTURE_LOCAL_ENGINE, INFRASTRUCTURE_PROVIDED_AWS]

    def __init__(
            self,
            user_data_plugin: UserDataBasePlugin,
            engine_account_id: Optional[str] = None, engine_project_id: Optional[str] = None, engine_api_key: Optional[str] = None,
            infrastructure_speech_synthesis: _INFRASTRUCTURE_TYPES_UNION = INFRASTRUCTURE_ENGINE,
            characters_voices: Optional[dict] = None, deployment: Optional[Deployment] = None,
            database_sessions_users_data: DatabaseSessionsUsersData = DatabaseSessionsUsersData(),
            database_messages_content: DatabaseMessagesContent = DatabaseMessagesContent(),
            database_users_notifications_subscriptions: DatabaseUsersNotificationsSubscriptions = DatabaseUsersNotificationsSubscriptions(),
            plugins: Plugins = Plugins(),
    ):
        self.user_data_plugin = user_data_plugin
        self.engine_account_id = engine_account_id
        self.engine_project_id = engine_project_id
        self.engine_api_key = engine_api_key
        self.infrastructure_speech_synthesis = infrastructure_speech_synthesis
        self.characters_voices = characters_voices
        self.deployment = deployment
        self.database_sessions_users_data = database_sessions_users_data
        self.database_messages_content = database_messages_content if database_messages_content is not None else dummy_object
        self.database_users_notifications_subscriptions = database_users_notifications_subscriptions if database_users_notifications_subscriptions is not None else dummy_object
        self.default_session_data_timeout = 60
        self.plugins = plugins if plugins is not None else list()  # We use a list instead of dummy object, since there is multiple for loop calls on this object

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
        raise_if_variable_not_expected_type_and_not_none(value=deployment, expected_type=Deployment, variable_name="deployment")
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


INFRASTRUCTURE_TO_BASE_URL: Dict[str, str] = {
    Settings.INFRASTRUCTURE_ENGINE: 'https://www.engine.inoft.com',
    Settings.INFRASTRUCTURE_NEXT_ENGINE: 'https://www.next.engine.inoft.com',
    Settings.INFRASTRUCTURE_LOCAL_ENGINE: 'http://127.0.0.1:5000',
    Settings.INFRASTRUCTURE_PROVIDED_AWS: 'not yet implemented'  # todo: allow a method to use boto3 instead of the engine API
}
