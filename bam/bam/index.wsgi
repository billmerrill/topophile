import base64
import datetime
import os
import tempfile
import json
import re
import topoconf

import cherrypy
import cove.model
import job

from models import STLModelService
from pricing import ModelPricing
from shapeways_service import ShapewaysService
from mako.template import Template
from mako.lookup import TemplateLookup

app_config = topoconf.prod_app_config
    
class TestyClass(object):
    exposed = True
    @cherrypy.expose
    def index(self):
        return "I went to stock market today. I did a business."

class RootClass(object):
    exposed = True
    def __init__(self):
        self.build = STLModelService(app_config)
        self.price = ModelPricing(app_config)
        self.vincent = TestyClass()
        self.printer = ShapewaysService(app_config)
        
def CORS():
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'


def application(environ, start_response):
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    conf = {
        '/': {
         'tools.sessions.on': True
         'tools.CORS.on': True
        },
        '/build': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
        '/price': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }}
        
    cherrypy.config.update({'environment': 'embedded'})
    cherrypy.tree.mount(RootClass(), script_name='/', config=conf)
    return cherrypy.tree(environ, start_response)
        

