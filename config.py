import os


class Config(object):
    BASE_URI = './'

    XMR_ADDR = os.environ.get('XMR_ADDR')

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
