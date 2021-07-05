# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

engine = Flask("app")

from .config import Configuration

engine.config.from_object(Configuration)
db = SQLAlchemy(engine,session_options={"autoflush": False})

SITE_URL = ""

from .views import *
