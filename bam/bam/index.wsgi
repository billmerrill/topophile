import base64
import datetime
import os
import tempfile
import json
import re

import cherrypy
import cove.model
import job

from models import STLModelService
from pricing import ModelPricing
from shapeways_service import ShapewaysService
from mako.template import Template
from mako.lookup import TemplateLookup


local_app_config = {'model_dir': os.path.join(os.getcwd(), "app/model_cache"),
              'elevation_dir': os.path.join(os.getcwd(), "app/elevation_cache"),
              'elevation_server': 'http://127.0.0.1/cgi-bin/mapserv?',
              'ms_scaling': True,
              'serial_store': os.path.join(os.getcwd(), "app/serial.no"),
              'app_url': "topophile.com/build1/" }
              
          
prod_home_dir = '/home/billmerrill/webapps/test_wsgi/htdocs'
prod_app_config = {'home_dir': prod_home_dir,
        'model_dir': os.path.join(prod_home_dir,  "app/model_cache"),
                'elevation_dir': os.path.join(prod_home_dir, "app/elevation_cache"),
                'elevation_server': 'http://billmerrill.webfactional.com/mapserver/mapserv?',
                'ms_scaling': True,
                'serial_store': os.path.join(prod_home_dir, "app/serial.no"),
                'app_url': "topophile.com/build/" }
              
              
app_config = prod_app_config
        
    
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
    # cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    conf = {
        '/': {
         'tools.sessions.on': True
        #  'tools.CORS.on': True
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
        

