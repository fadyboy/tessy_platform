from flask import Blueprint

bp = Blueprint("auth", __name__)

from studentapp.auth import email, forms, routes
