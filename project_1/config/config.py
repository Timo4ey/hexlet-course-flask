import os


class Configuration():
    DEBUG = True
    SECRET_KEY = os.urandom(32)
    SESSION_TYPE = 'filesystem'
