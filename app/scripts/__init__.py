# -*- coding: utf-8 -*-

from app import db
from .initializedb import init_database

def initdb():
    init_database(db)

    print("Initialized default DB")
