import os

local_app_config = {'model_dir': os.path.join(os.getcwd(), "app/model_cache"),
              'elevation_dir': os.path.join(os.getcwd(), "app/elevation_cache"),
              'elevation_server': 'http://127.0.0.1/cgi-bin/mapserv?',
              'map_file_dir': '/Library/WebServer/Documents/cay/',
              'map_file': '/Library/WebServer/Documents/cay/new-srtm-wcs.map',
              'ms_scaling': True,
              'serial_store': os.path.join(os.getcwd(), "app/serial.no"),
              'app_url': "topophile.com/build1/",
              'model_home_url': 'http://127.0.0.1:9999/' }
              
          
prod_app_config = {
                'elevation_server': 'http://billmerrill.webfactional.com/mapserver/mapserv.cgi?',
                'model_home_url':   'http://billmerrill.webfactional.com/1/',
                'model_dir':        '/home/billmerrill/webapps/model_cache',
                'elevation_dir':    '/home/billmerrill/topo-cache/b1/elevation_cache',
                'serial_store':     '/home/billmerrill/topo-cache/b1/serial.no',
                'map_file_dir':     '/home/billmerrill/releases/vcs/topophile/cay',
                'map_file':         '/home/billmerrill/releases/vcs/topophile/cay/prod-srtm-wcs.map',
                'ms_scaling':       True,
                'app_url':          'topophile.com/build/'}
              

new_local_app_config = {
                'elevation_server': 'http://127.0.0.1/cgi-bin/mapserv?',
                'model_home_url':   'http://127.0.0.1:9999/',
                'model_dir':        os.path.join(os.getcwd(), "apptest/model_cache"),
                'elevation_dir':    os.path.join(os.getcwd(), "apptest/elevation_cache"),
                'serial_store':     os.path.join(os.getcwd(), "apptest/serial.no"),
                'map_file_dir':     '/Library/WebServer/Documents/cay/',
                'map_file':         '/Library/WebServer/Documents/cay/new-srtm-wcs.map',
                'ms_scaling':       True,
                'app_url':          'topophile.com/build/'}
              