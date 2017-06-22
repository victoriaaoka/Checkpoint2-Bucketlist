from flask import Blueprint

# This is an instance of Blueprint that represents the authentication blueprint
auth_blueprint = Blueprint('auth', __name__)

from . import views