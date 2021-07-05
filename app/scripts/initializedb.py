# -*- coding: utf-8 -*-

from ..models.product import Product

def init_database(db):
    db.drop_all()
    db.create_all()
