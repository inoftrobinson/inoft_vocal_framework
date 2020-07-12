from typing import Optional

from flask import Flask, render_template, request, jsonify
import json

from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.web_interface.backend import get_list_content

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", list_content=content_list(),
                           filepath="F:/Inoft/anvers_1944_project/inoft_vocal_engine/botpress_integration/builtin_text.json")

@app.route("/audio-editor/<project_id>")
def audio_editor(project_id: str):
    # todo: look for project id in database
    static_data = {'Collections': {'Tracks': {'models': [{'attributes': {
        'buffer': {'duration': 167.714, 'length': 8050272, 'numberOfChannels': 2, 'sampleRate': 48000},
        'color': '#00a0b0', 'file': {'lastModified': 1591264478848, 'name': 'jean sablon - alexa.mp3', 'size': 1007568,
                                     'type': 'audio/mpeg', 'webkitRelativePath': ''}, 'gain': 1, 'length': 1920,
        'muted': False, 'name': 'Track 1', 'pan': 0.5, 'solo': False}}]}}}

    return render_template("audio-editor/index.html", project_id=project_id, project_data=static_data)

@app.route("/audio-editor/<project_id>/save", methods=["POST"])
def audio_editor_save(project_id: str):
    print(f"Saved for {project_id}")
    print(request.get_json())
    data = SafeDict(request.get_json())
    audiee_object = data.get("Audiee").to_dict(default=None)
    print(audiee_object)
    return jsonify({"success": True})

@app.route("/diagrams")
def diagrams():
    return render_template("diagrams/index.html")


@app.route("/project_dir",  methods=["POST"])
def change_project_dir():
    data = SafeDict(request.get_json())
    filepath = data.get("filepath").to_str(default=None)
    list_content = content_list(filepath=filepath)
    return jsonify({"html": list_content})

def content_list(filepath: Optional[str] = None):
    if filepath is None:
        contents = list()
    else:
        contents = get_list_content(filepath=filepath)
    return render_template("list_content_elements/list.html", elements=contents)


"""
@app.errorhandler(404)
def error_404(error):
    return None
    return render_template("error_404.html")
"""

if __name__ == '__main__':
    app.run()
