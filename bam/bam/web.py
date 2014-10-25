import cherrypy
import cove.model

class STLModelService(object):
    exposed = True

    # @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return 'wee'
        
    #def POST(self, elevation, nwlat, nwlon, selat, selon, size=200, rez=50):
    def POST(self, elevation, size=200, rez=50):
        copy_elevation_filename = "elevation_cache.tif" 
        # XXX we need to copy the elevation file in so we can gdal.Open 
        
        fn = self._build_model(elevation.file.name, int(size), int(rez))
        return fn

    def _build_model(self, elevation, size, rez):
        model_config = { 'src': 'test-data/mtr-sq.tif',
                         'output_resolution': rez,
                         'output_physical_max': size }
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