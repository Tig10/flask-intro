import os

# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = b'\x9b2\xe9\xb9t\x9cA\xecu\x9d\xcd\xa9PXK\x12\xa1\xdf\xc0\x00\xdf\x02-\x02'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False