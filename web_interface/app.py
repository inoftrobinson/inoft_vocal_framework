from datetime import datetime
from typing import Optional

from flask import Flask, Response, render_template, request, jsonify
import json

from inoft_vocal_engine.databases.dynamodb.audio_editor_projects_dynamodb_client import AudioEditorProjectsDynamoDbClient
from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import ProjectsTextContentsDynamoDbClient
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.web_interface.backend.audio_editor import audio_editor_blueprint
from inoft_vocal_engine.web_interface.backend.diagrams import diagrams_blueprint
from inoft_vocal_engine.web_interface.backend.team_organization import organization_blueprint
from inoft_vocal_engine.web_interface.static_clients import project_resources

app = Flask(__name__)
app.register_blueprint(audio_editor_blueprint)
app.register_blueprint(organization_blueprint)
app.register_blueprint(diagrams_blueprint)


@app.route("/")
def index():
    return render_template("index.html", list_content=content_list(),
                           filepath="F:/Inoft/anvers_1944_project/inoft_vocal_engine/botpress_integration/builtin_text.json")

@app.route("/text")
def text():
    return render_template("text-editor/test.html")

@app.route("/equalizer")
def equalizer():
    return render_template("equalizer/index.html")

@app.route("/project_dir",  methods=["POST"])
def change_project_dir():
    data = SafeDict(request.get_json())
    filepath = data.get("filepath").to_str(default=None)
    # list_content = content_list(filepath=filepath)
    # return jsonify({"html": list_content})

def content_list():
    # contents_items = get_list_content(filepath=filepath)
    content_items = project_resources.project_text_contents_dynamodb_client.get_latest_updated(num_latest_items=30).items
    return render_template("list_content_elements/list.html", elements=content_items)

@app.route("/text-contents/update/<element_id>", methods=["POST"])
def update_text_content(element_id: str):
    print(element_id)
    request_json_data = SafeDict(request.get_json())
    dialogue_line_index = request_json_data.get("dialogueLineIndex").to_int(default=None)
    element_text = request_json_data.get("text").to_str(default=None)

    project_resources.project_text_contents_dynamodb_client.update_content_element(
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
