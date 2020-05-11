from flask import Blueprint

bp = Blueprint("main", __name__)

from studentapp.main import forms, routes