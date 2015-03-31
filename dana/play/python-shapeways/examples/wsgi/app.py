import json

from shapeways.client import Client

client = Client(
    consumer_key="fa206ebf6c8e642d3ed0e4ee7be72e1ba4266f37",
    consumer_secret="06db7be844acc56473ac6ca8998cc2e50656e019",
    callback_url="http://localhost:3000/callback"
)

def application(environ, start_response):
    url = environ["PATH_INFO"]
    if url.startswith("/favicon.ico"):
        start_response("204 No Content", [])
        return [""]
    elif url.startswith("/login"):
        url = client.connect()
        start_response("302 Found", [
            ("Location", str(url)),
        ])
        return [""]
    elif url.startswith("/callback"):
        print 'query string', environ["QUERY_STRING"]
        client.verify_url(environ["QUERY_STRING"])
        start_response("302 Found", [
            ("Location", "http://localhost:3000/"),
        ])
        return [""]
    elif url.startswith("/models"):
        r = client.get_models()
        start_response("200 Ok", [
            ("Content-Type", "application/json"),
        ])
        return [json.dumps(r)   ]
    else:
        response = client.get_api_info()
        response['oauth_token'] = client.oauth_token
        response['oauth_secret'] = client.oauth_secret
        
        start_response("200 Ok", [
            ("Content-Type", "application/json"),
        ])
        return [json.dumps(response)]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    try:
        httpd = make_server("", 3000, application)
        print "Tracking Server Listening on Port 3000..."
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Exiting..."
