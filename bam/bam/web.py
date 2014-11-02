import tempfile
import cherrypy
import cove.model
import job

class STLModelService(object):
    exposed = True
    
    def GET(self, nwlat, nwlon, selat, selon, size, rez):
        '''
        use the bounding box to query for elevation data, and build a model
        return the stl file
        '''
        gig = job.BoundingBoxJob(nwlat, nwlon, selat, selon, size, rez)
        model_fn = gig.run()
        
        return model_fn
        
    def POST(self, elevation, size=200, rez=50):
        '''
        accept an uploaded geotiff, return an stl model
        '''
        elevation_data = tempfile.NamedTemporaryFile(delete=False)
        try:
            while True:
                data = elevation.file.read(1024)
                if not data:
                    break
                elevation_data.write(data)
                
            elevation_data.seek(0)
            elevation_data.flush()
            
            gig = job.GeoTiffJob(elevation_data.name, size, rez)
            model_fn = gig.run()
        finally:
            elevation_data.close()
            
        return model_fn

def CORS():
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'


if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    conf = {
        '/': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.sessions.on': True,
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'text/plain')],
         'tools.CORS.on': True
        }
    }
    cherrypy.quickstart(STLModelService(), '/', conf)