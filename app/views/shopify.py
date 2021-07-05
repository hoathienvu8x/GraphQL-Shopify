# -*- coding: utf-8 -*-

from app import engine, SITE_URL

@engine.route('/')
def home_page():
    return 'I\'ts Works!'
