import os


class Config:
    PATH_BASE = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}/db/music.db".format(PATH_BASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '\x80\xdf4\x0c*\xff0W\xa4\xe2\xce2\xe6\xec)\x98\xce\x97\xc8^7\x84\x17Y'

BASE_PATH = os.path.dirname(os.path.realpath(__file__).replace('\\', '/'))
