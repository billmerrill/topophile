import tempfile
import cherrypy
import cove.model
import job
class STLModelService(object):
    exposed = True

    # @cherrypy.tools.accept(media='text/plain')
    def GET(self, nwlat, nwlon, selat, selon, size, rez):
        gig = job.ModelJob(nwlat, nwlon, selat, selon, size, rez)
        model_fn = gig.run()
        return model_fn
        
    #def POST(self, elevation, nwlat, nwlon, selat, selon, size=200, rez=50):
    def POST(self, elevation, size=200, rez=50):
        elevation_data = tempfile.NamedTemporaryFile(delete=False)
        try:
            while True:
                data = elevation.file.read(100000)
                if not data:
                    break
                elevation_data.write(data)
                
            elevation_data.seek(0)
            elevation_data.flush()
            
            # XXX we need to copy the elevation file in so we can gdal.Open 
            
            fn = self._build_model(elevation_data.name, int(size), int(rez))
        finally:
            elevation_data.close()
            
        return fn

    def _build_model(self, elevation_filename, size, rez):
        model_config = { 'src': elevation_filename,
                         'dst': 'test-data/latest-output.stl',
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