from flask import Blueprint, render_template

diagrams_blueprint = Blueprint("diagrams", __name__, template_folder="templates")

@diagrams_blueprint.route('/diagrams')
def diagrams():
    return render_template("diagrams/index.html")
