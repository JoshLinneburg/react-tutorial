import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CORS_HEADERS = ["Content-Type", "Authorization"]
    JSON_SORT_KEYS = False
    FUSIONAUTH_API_KEY = os.environ.get("FUSIONAUTH_API_KEY")
    RESULTS_PER_PAGE = os.environ.get("RESULTS_PER_PAGE") or 10
    SECRET_KEY = os.environ.get("SECRET_KEY") or "changeme"
    JWT_SECRET_KEY = SECRET_KEY
    TESTING = os.environ.get("TESTING") or False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///" + os.path.join(
        basedir, "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS") or False
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=90)
    JWT_CSRF_METHODS = os.environ.get("JWT_CSRF_METHODS") or []
    JWT_ALGORITHM = "HS512"
