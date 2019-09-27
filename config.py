import os

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config:
    DEBUG = False
    ENV = os.getenv('ENV')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    pass


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
