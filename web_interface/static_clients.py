from inoft_vocal_engine.databases.dynamodb.audio_editor_projects_dynamodb_client import AudioEditorProjectsDynamoDbClient
from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import ProjectsTextContentsDynamoDbClient
from inoft_vocal_engine.databases.dynamodb.team_organization_projects_dynamodb_client import TeamOrganizationProjectsDynamoDbClient
from inoft_vocal_engine.web_interface.account_ressources import AccountResources
from inoft_vocal_engine.web_interface.project_ressources import ProjectResources

project_resources = ProjectResources(account_resources=AccountResources(account_id="robinsonlabourdette"), project_name="anvers1944")

"""
class StaticClients:
    _audio_editor_projects_dynamodb_static_client = None
    _projects_text_contents_dynamodb_static_client = None
    _team_organization_projects_dynamodb_static_client = None

    @property
    def audio_editor_projects_dynamodb_static_client(self) -> AudioEditorProjectsDynamoDbClient:
        if StaticClients._audio_editor_projects_dynamodb_static_client is None:
            StaticClients._audio_editor_projects_dynamodb_static_client = AudioEditorProjectsDynamoDbClient(
                table_name="inoft-vocal-engine-audio-projects-data", region_name="eu-west-2"
            )
        return StaticClients._audio_editor_projects_dynamodb_static_client

    @property
    def projects_text_contents_dynamodb_static_client(self) -> ProjectsTextContentsDynamoDbClient:
        if StaticClients._projects_text_contents_dynamodb_static_client is None:
            StaticClients._projects_text_contents_dynamodb_static_client = ProjectsTextContentsDynamoDbClient(
                table_name="inoft-vocal-engine-project-test-2", region_name="eu-west-2"
            )
        return StaticClients._projects_text_contents_dynamodb_static_client

    @property
    def team_organization_projects_dynamodb_static_client(self) -> TeamOrganizationProjectsDynamoDbClient:
        if StaticClients._team_organization_projects_dynamodb_static_client is None:
            StaticClients._team_organization_projects_dynamodb_static_client = TeamOrganizationProjectsDynamoDbClient(
                table_name="inoft-vocal-engine-project-organization-test-1", region_name="eu-west-2"
            )
        return StaticClients._team_organization_projects_dynamodb_static_client
"""