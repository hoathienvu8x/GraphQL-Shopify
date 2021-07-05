# -*- coding: utf-8 -*-

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField

from .product import ProductObject

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_products = SQLAlchemyConnectionField(ProductObject)

schema = graphene.Schema(query=Query)
