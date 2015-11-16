import json


class ModelStub(object):
    exposed = True

    def GET(self, *args, **kwargs):
        '''
        use the bounding box to query for elevation data, and build a model
        return the stl file
        '''
        model = {'url': "http://127.0.0.1:9999/3E225D98-E9FE-458F-A1D2-EFD54FCBAF26.stl",
                 'x-size': 100.0,
                 'y-size': 75.0,
                 'z-size': 90.0}
        return json.dumps(model)
