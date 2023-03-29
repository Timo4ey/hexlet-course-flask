import os


class Configuration():
    DEBUG = False
    SECRET_KEY = os.urandom(32)
    SESSION_TYPE = 'filesystem'
