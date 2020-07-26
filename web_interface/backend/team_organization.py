from flask import Blueprint, render_template

organization_blueprint = Blueprint("organization", __name__, template_folder="templates")

@organization_blueprint.route('/organization')
def organization():
    return render_template("team-organization/gantt.html")
