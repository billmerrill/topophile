import os

local_app_config = {'model_dir': os.path.join(os.getcwd(), "app/model_cache"),
              'elevation_dir': os.path.join(os.getcwd(), "app/elevation_cache"),
              'elevation_server': 'http://127.0.0.1/cgi-bin/mapserv?',
              'map_file_dir': '/Library/WebServer/Documents/cay/',
              'ms_scaling': True,
              'serial_store': os.path.join(os.getcwd(), "app/serial.no"),
              'app_url': "topophile.com/build1/" }
              
          
prod_home_dir = '/home/billmerrill/webapps/test_wsgi/htdocs'
prod_app_config = {'home_dir': prod_home_dir,
        'model_dir': os.path.join(prod_home_dir,  "app/model_cache"),
                'elevation_dir': os.path.join(prod_home_dir, "app/elevation_cache"),
                'elevation_server': 'http://billmerrill.webfactional.com/mapserver/mapserv?',
                'map_file_dir': '/Library/WebServer/Documents/cay/',
                'ms_scaling': True,
                'serial_store': os.path.join(prod_home_dir, "app/serial.no"),
                'app_url': "topophile.com/build/" }
              