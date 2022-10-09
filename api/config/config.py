import os
from decouple import config
from datetime import timedelta

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

uri = config("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

class Config:
    SECRET_KEY=config('SECRET_KEY','Secret')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')
    
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI="postgresql://realiz3d:1234@localhost/carshop_flask"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    DEBUG=True

class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI="sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True

config_dict={
    'dev':DevConfig,
    'testing':TestConfig,
}