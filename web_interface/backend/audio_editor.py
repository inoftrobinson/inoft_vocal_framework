from flask import Blueprint, render_template, jsonify, request

from inoft_vocal_engine.nested_object_to_dict_with_auto_type_checking import NestedObjectToDict
from inoft_vocal_engine.web_interface.backend.audio_project import AudioProject
from inoft_vocal_engine.web_interface.static_clients import StaticClients

audio_editor_blueprint = Blueprint("audio-editor", __name__, template_folder="templates")

dice = {
    'projectId': 'builtin_text-lbs0Re',
    'collections': {
        'tracks': {
            'models': [{
                'attributes': {
                    'file': {
                        'name': 'jean sablon - alexa.mp3',
                        'webkitRelativePath': '',
                        'lastModified': 1591264478848.0,
                        'size': 1007568.0,
                        'type': 'audio/mpeg'
                    },
                    'color': '#00a0b0',
                    'length': 1920.0,
                    'name': 'Track 1',
                    'solo': False,
                    'buffer': {
                        'duration': 167.71,
                        'length': 7396188.0,
                        'sampleRate': 44100.0,
                        'numberOfChannels': 2.0
                    },
                    'pan': 0,
                    'muted': False,
                    'gain': 1.0,
                }
            }]
        }
    }
}

if __name__ == "__main__":
    audio_project = AudioProject(**dice)
    audio_project.add_track()
    print(audio_project)

@audio_editor_blueprint.route("/audio-editor/<project_id>")
def audio_editor(project_id: str):
    audio_project_data, audio_request_success = StaticClients().audio_editor_projects_dynamodb_static_client.get_project_data_by_project_id(project_id=project_id)
    text_project_data, text_request_success = StaticClients().projects_text_contents_dynamodb_static_client.get_by_id(project_id=project_id)
    # audio_project = NestedObjectToDict.dict_to_typed_class(class_type=AudioProject, data_dict=audio_project_data)
    # print(f"audio_project = {audio_project}")
    print(f"audio_project_data = {audio_project_data}\n& text_project_data = {text_project_data}")

    static_data = {'Collections': {'Tracks': {'models': [{'attributes': {
        'buffer': {'duration': 167.714, 'length': 8050272, 'numberOfChannels': 2, 'sampleRate': 48000},
        'color': '#00a0b0', 'file': {'lastModified': 1591264478848, 'name': 'jean sablon - alexa.mp3', 'size': 1007568,
                                     'type': 'audio/mpeg', 'webkitRelativePath': ''}, 'gain': 1, 'length': 1920,
        'muted': False, 'name': 'Track 1', 'pan': 0.5, 'solo': False}}]}}}

    return render_template("audio-editor/index.html", project_id=project_id, project_data=audio_project_data)

@audio_editor_blueprint.route("/audio-editor/<project_id>/save", methods=["POST"])
def audio_editor_save(project_id: str):
    print(f"Saving data for project {project_id}")

    request_json_data = request.get_json()
    if request_json_data is not None:
        request_success = StaticClients().audio_editor_projects_dynamodb_static_client.save_project_data(project_id=project_id,
                                                                                                         project_data=request_json_data)
    else:
        request_success = False

    return jsonify({"success": request_success})
