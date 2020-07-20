from datetime import datetime
from typing import Optional

from flask import Flask, Response, render_template, request, jsonify
import json

from inoft_vocal_engine.databases.dynamodb.audio_editor_projects_dynamodb_client import AudioEditorProjectsDynamoDbClient
from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import ProjectsTextContentsDynamoDbClient
from inoft_vocal_engine.safe_dict import SafeDict

app = Flask(__name__)
audio_edtor_projects_dynamodb_static_client = AudioEditorProjectsDynamoDbClient(
    table_name="inoft-vocal-engine-audio-projects-data", region_name="eu-west-2"
)
projects_text_contents_dynamodb_static_client = ProjectsTextContentsDynamoDbClient(
    table_name="inoft-vocal-engine-project-test-2", region_name="eu-west-2"
)


@app.route("/")
def index():
    return render_template("index.html", list_content=content_list(),
                           filepath="F:/Inoft/anvers_1944_project/inoft_vocal_engine/botpress_integration/builtin_text.json")

@app.route("/text")
def text():
    return render_template("text-editor/test.html")

@app.route("/audio-editor/<project_id>")
def audio_editor(project_id: str):
    # todo: look for project id in database
    project_data, request_success = audio_edtor_projects_dynamodb_static_client.get_project_data_by_project_id(project_id=project_id)
    print(f"resumed data = {project_data}")

    static_data = {'Collections': {'Tracks': {'models': [{'attributes': {
        'buffer': {'duration': 167.714, 'length': 8050272, 'numberOfChannels': 2, 'sampleRate': 48000},
        'color': '#00a0b0', 'file': {'lastModified': 1591264478848, 'name': 'jean sablon - alexa.mp3', 'size': 1007568,
                                     'type': 'audio/mpeg', 'webkitRelativePath': ''}, 'gain': 1, 'length': 1920,
        'muted': False, 'name': 'Track 1', 'pan': 0.5, 'solo': False}}]}}}

    return render_template("audio-editor/index.html", project_id=project_id, project_data=project_data)

@app.route("/audio-editor/<project_id>/save", methods=["POST"])
def audio_editor_save(project_id: str):
    print(f"Saving data for project {project_id}")

    request_json_data = request.get_json()
    request_json_data["projectId"] = project_id
    if request_json_data is not None:
        request_success = audio_edtor_projects_dynamodb_static_client.save_project_data(project_data=request_json_data)
    else:
        request_success = False

    return jsonify({"success": request_success})

@app.route("/diagrams")
def diagrams():
    return render_template("diagrams/index.html")


@app.route("/project_dir",  methods=["POST"])
def change_project_dir():
    data = SafeDict(request.get_json())
    filepath = data.get("filepath").to_str(default=None)
    # list_content = content_list(filepath=filepath)
    # return jsonify({"html": list_content})

def content_list():
    # contents_items = get_list_content(filepath=filepath)
    content_items = projects_text_contents_dynamodb_static_client.get_latest_updated(num_latest_items=30).items
    return render_template("list_content_elements/list.html", elements=content_items)

@app.route("/text-contents/update/<element_id>", methods=["POST"])
def update_text_content(element_id: str):
    print(element_id)
    request_json_data = SafeDict(request.get_json())
    dialogue_line_index = request_json_data.get("dialogueLineIndex").to_int(default=None)
    element_text = request_json_data.get("text").to_str(default=None)

    projects_text_contents_dynamodb_static_client.update_content_element(
        element_id=element_id, dialogue_line_index=dialogue_line_index, element_text=element_text)

    print(request_json_data)
    return Response(status=200)


"""
@app.errorhandler(404)
def error_404(error):
    return None
    return render_template("error_404.html")
"""

if __name__ == '__main__':
    app.run()
