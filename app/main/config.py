import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    DEBUG = False
    JWT_EXP = 8
    ACTIVATION_EXP_DAYS = 3

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "development"
    HOST = "localhost"

    RESTX_MASK_SWAGGER = False
    MAIL_DEBUG = False
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_SUPPRESS_SEND = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

class StagingConfig(Config):
    DEBUG = True
    LOG_LEVEL = "INFO"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "staging"
    HOST = "0.0.0.0"

class TestingConfig(Config):
    DEBUG = True
    LOG_LEVEL = "WARNING"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "testing"


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "ERROR"
    ENV = "production"


config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
    "staging": StagingConfig,
}

env_name = os.environ.get("ENV_NAME") or "dev"
app_config = config_by_name[env_name]
