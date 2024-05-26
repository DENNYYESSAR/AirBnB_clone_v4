#!/usr/bin/python3
""" Blueprint setup for API v1 views """
from flask import Blueprint

app_views = Blueprint('/api/v1', __name__, url_prefix='/api/v1')

# Import all views from the package api.v1.views.index
# PEP8 will complain about this wildcard import, but it's required here
from api.v1.views.index import *
from api.v1.views.states import *
