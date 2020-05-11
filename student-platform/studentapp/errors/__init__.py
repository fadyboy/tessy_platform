from flask import Blueprint

bp = Blueprint("errors", __name__)

# import at botton to avoid circular dependencies
from studentapp.errors import handlers
