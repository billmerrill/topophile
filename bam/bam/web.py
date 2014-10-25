import cherrypy
import cove.model

class STLModelService(object):
    exposed = True

    # @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return 'wee'
        
    def POST(self, nwlat, nwlon, selat, selon, size=200, rez=50):
        fn = self._build_model()
        return fn

    def _build_model(self):
        model_config = { 'src': 'test-data/mtr-sq.tif',
                         'output_resolution_max': 100,
                         'output_physical_max': 200 }
        model = cove.model.SolidElevationModel(model_config)
        return model.build_stl()

     

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