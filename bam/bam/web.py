import cherrypy

class STLModelService(object):
    exposed = True

    # @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return 'wee'
        
    def POST(self, nwlat, nwlon, selat, selon, size=200, rez=50):
        model_url = '/model.stl'
        return model_url
     

if __name__ == '__main__':
    conf = {
        '/': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.sessions.on': True,
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(STLModelService(), '/', conf)