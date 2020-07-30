import os
from typing import Optional, Type
from pydantic.dataclasses import dataclass

from inoft_vocal_engine.cloud_providers.aws.deploy_utils import DeployHandler
from inoft_vocal_engine.databases.dynamodb.audio_editor_projects_dynamodb_client import AudioEditorProjectsDynamoDbClient
from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import ProjectsTextContentsDynamoDbClient
from inoft_vocal_engine.databases.dynamodb.team_organization_projects_dynamodb_client import TeamOrganizationProjectsDynamoDbClient
from inoft_vocal_engine.web_interface.account_ressources import AccountResources


@dataclass
class ProjectResources:
    account_resources: AccountResources
    project_name: str
    _audio_editor_projects_dynamodb_client = None
    _project_text_contents_dynamodb_client = None
    _team_organization_projects_dynamodb_client = None

    def __post_init_post_parse__(self):
        self._audio_editor_projects_dynamodb_table_name = f"{self.account_resources.account_id}_{self.project_name}_audio-editor-projects"
        self._project_text_contents_dynamodb_table_name = f"{self.account_resources.account_id}_{self.project_name}_project-text-contents"
        self._team_organization_projects_dynamodb_table_name = f"{self.account_resources.account_id}_{self.project_name}_team-organization"

    # todo: check if making the database clients static is actually a good idea or not
    #  (with a ton of users, it might be too much for the static memory of a lambda)
    @property
    def audio_editor_projects_dynamodb_client(self) -> AudioEditorProjectsDynamoDbClient:
        print(f"table_name audio = {self._audio_editor_projects_dynamodb_table_name}")
        if self._audio_editor_projects_dynamodb_client is None:
            self._audio_editor_projects_dynamodb_client = AudioEditorProjectsDynamoDbClient(
                table_name=self._audio_editor_projects_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._audio_editor_projects_dynamodb_client

    @property
    def project_text_contents_dynamodb_client(self) -> ProjectsTextContentsDynamoDbClient:
        if self._project_text_contents_dynamodb_client is None:
            self._project_text_contents_dynamodb_client = ProjectsTextContentsDynamoDbClient(
                table_name=self._project_text_contents_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._project_text_contents_dynamodb_client

    @property
    def team_organization_projects_dynamodb_client(self) -> TeamOrganizationProjectsDynamoDbClient:
        if self._team_organization_projects_dynamodb_client is None:
            self._team_organization_projects_dynamodb_client = TeamOrganizationProjectsDynamoDbClient(
                table_name=self._team_organization_projects_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._team_organization_projects_dynamodb_client

    def deploy_lambda(self):
        import inoft_vocal_engine
        inoft_vocal_engine_root_dirpath = os.path.dirname(os.path.dirname(os.path.abspath(inoft_vocal_engine.__file__)))
        DeployHandler().deploy(lambda_files_root_folderpath=inoft_vocal_engine_root_dirpath,
                               bucket_name="inoft-vocal-engine-web-test",
                               bucket_region_name="eu-west-3",
                               lambda_name="inoft-vocal-engine-web-interface",
                               lambda_handler="app.app", runtime="python3.7")


if __name__ == "__main__":
    resources = ProjectResources(account_resources=AccountResources(account_id="robinsonlabourdette"), project_name="anvers1944")
    resources.deploy_lambda()
