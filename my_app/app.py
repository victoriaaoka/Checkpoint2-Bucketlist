import os
from flask import redirect, url_for
from flask_api import FlaskAPI
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config


db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    Swagger(app)
    # app.config.from_object(os.getenv('DATABASE_URL'))
    # app.config.from_pyfile('config.py')
    app.config.from_object(app_config[config_name])
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config.get('SECRET')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/Bucketlistdb'
    db.init_app(app)
    @app.route("/")
    def index():
        url = url_for("flasgger.apidocs")
        return redirect(url,  code=302)
    from my_app.views import auth_blueprint, bucketlist_blueprint, bucketlist_item_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    app.register_blueprint(bucketlist_blueprint, url_prefix='/api/v1')
    app.register_blueprint(bucketlist_item_blueprint, url_prefix='/api/v1')

    return app
