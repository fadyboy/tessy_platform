from flask import render_template
from studentapp.errors import bp
from studentapp import db


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500
