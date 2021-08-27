from config import Config
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
cors = CORS()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app=app)
    ma.init_app(app=app)
    migrate.init_app(app=app, db=db)
    cors.init_app(app=app)

    from flask_app.users.routes import users_bp
    app.register_blueprint(users_bp)

    return app


from flask_app.models import *
