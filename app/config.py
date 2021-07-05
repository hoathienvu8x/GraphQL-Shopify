# -*- coding: utf-8 -*-

import os

class Config(object):
    DEBUG = False
    TESTING = False

SQLALCHEMY_DATABASE_PATH = "{}".format(os.path.join(os.path.dirname(os.path.realpath(__file__)),"database"))

class Configuration(Config):
    ENV = "development"
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(SQLALCHEMY_DATABASE_PATH, "shopify.db"))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    PORT = 4000
