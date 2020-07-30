import json
from flask import Blueprint, render_template, Response, request, jsonify
from inoft_vocal_engine.web_interface.static_clients import project_resources

organization_blueprint = Blueprint("organization", __name__, template_folder="templates")

@organization_blueprint.route("/organization/<project_id>")
def organization(project_id: str):
    project_data, request_success = project_resources.team_organization_projects_dynamodb_client.get_project_data_by_project_id(project_id=project_id)
    print(f"project_data = {project_data}")
    return render_template("team-organization/gantt.html", project_id=project_id, resumed_project_data=json.dumps(project_data))

@organization_blueprint.route("/organization/save/<project_id>", methods=["POST"])
def organization_save(project_id: str):
    request_json_data = request.get_json()
    print(request_json_data)
    project_resources.team_organization_projects_dynamodb_client.save_project_data(project_id=project_id, project_data=request_json_data)
    return Response(status=201)
