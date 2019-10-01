from flask import Flask, render_template
from config import config
from flask_restplus import Api
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

CONFIG = ''
db = SQLAlchemy()
ma = Marshmallow()


def create_app(env, additional_settings={}):
    global CONFIG
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_object(config[env])

    config[env].init_app(app)
    app.config.update(additional_settings)

    db.init_app(app)
    ma.init_app(app)
    from api.models import order
    migrate = Migrate(app, db, compare_type=True)

    # Namespace
    from api.main import api as api_nsp
    api = Api(version="1.0",
              title="EnSa API Module",
              doc='/docs')
    api.add_namespace(api_nsp, path='')
    api.init_app(app)

    return app
