import os

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config
from my_app.models import db
from my_app.views import auth_blueprint, bucketlist_blueprint, bucketlist_item_blueprint

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(os.getenv('DATABASE_URL'))
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/Bucketlistdb'
    db.init_app(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(bucketlist_blueprint)
    app.register_blueprint(bucketlist_item_blueprint)

    return app
