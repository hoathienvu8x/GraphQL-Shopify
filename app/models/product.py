# -*- coding: utf-8 -*-

from app import db
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.DECIMAL, default=0)
    sale = db.Column(db.DECIMAL, default=0)

    def __repr__(self):
        return '<Product#{}{}/>'.format(self.id,"[{}]".format(self.name) if self.name else "")

class ProductObject(SQLAlchemyObjectType):
    class Meta:
        model = Product
        interfaces = (graphene.relay.Node, )
