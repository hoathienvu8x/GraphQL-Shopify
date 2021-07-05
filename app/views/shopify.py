# -*- coding: utf-8 -*-

from app import engine, SITE_URL
from flask_graphql import GraphQLView
from ..models.query import schema

engine.add_url_rule(
    '/graphql',
    view_func = GraphQLView.as_view(
        'graphql',
        schema = schema,
        graphiql = True
    )
)

@engine.route('/')
def home_page():
    return 'I\'ts Works!'
