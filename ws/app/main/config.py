import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB_URI = "postgresql://{0}:{1}@{2}:5432/{3}"
DATABASE_MASTER_USER = "postgres"
DATABASE_MASTER_PASSWORD = "postgres"
DATABASE_ADDRESS = "localhost"
DATABASE_NAME = "aws_basics"

FAIL_MSG = "'{}' parameter not specified, default {} will be used.."


def _get_db_url_point_from_env():
    global DATABASE_MASTER_USER
    v = _get_db_param_from_env('DATABASE_MASTER_USER', FAIL_MSG.format('DATABASE_MASTER_USER', 'user'))
    if v:
        DATABASE_MASTER_USER = v

    global DATABASE_MASTER_PASSWORD
    v = _get_db_param_from_env('DATABASE_MASTER_PASSWORD', FAIL_MSG.format('DATABASE_MASTER_PASSWORD', 'password'))
    if v:
        DATABASE_MASTER_PASSWORD = v

    global DATABASE_ADDRESS
    v = _get_db_param_from_env('DATABASE_ADDRESS', FAIL_MSG.format('DATABASE_ADDRESS', 'database url'))
    if v:
        DATABASE_ADDRESS = v

    global DATABASE_NAME
    v = _get_db_param_from_env('DATABASE_NAME', FAIL_MSG.format('DATABASE_NAME', 'database name'))
    if v:
        DATABASE_NAME = v


    global DEFAULT_DB_URI
    DEFAULT_DB_URI = DEFAULT_DB_URI.format(DATABASE_MASTER_USER, DATABASE_MASTER_PASSWORD, DATABASE_ADDRESS, DATABASE_NAME)


def _get_db_param_from_env(param_name, fail_msg):
    if param_name in os.environ:
        return os.environ[param_name]
    else:
        print(fail_msg)
        return None


class Config:
    DEBUG = True
    _get_db_url_point_from_env()


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DEFAULT_DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir


class ProductionConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = DEFAULT_DB_URI

    # if 'DATABASE_URL' in os.environ:
    #     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)