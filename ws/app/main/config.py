import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB_URI = "postgresql://postgres:postgres@localhost:5432/aws_basics"


class Config:
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DEFAULT_DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DEFAULT_DB_URI

    if os.environ['DATABASE_URL']:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    else:
        raise ConnectionError("DATABASE_URL is not set")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)