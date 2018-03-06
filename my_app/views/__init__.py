from flask import Blueprint

# This is an instance of Blueprint that represents the authentication blueprint
auth_blueprint = Blueprint('auth', __name__)
from . import auth

bucketlist_blueprint = Blueprint('bucketlist', __name__)
from . import bucketlist


bucketlist_item_blueprint = Blueprint('bucketlist_item', __name__)
from . import bucketlist_item
