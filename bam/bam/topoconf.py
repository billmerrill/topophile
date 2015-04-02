import os

PROD = 'prod'
DEV = 'dev'

prod_app_config = {
                'env':      PROD,
                'elevation_server': 'http://topophile.com/mapserver/mapserv.cgi?',
                'model_home_url':   'http://www.topophile.com/1/',
                'model_dir':        '/home/billmerrill/webapps/model_cache',
                'elevation_dir':    '/home/billmerrill/topo-cache/b1/elevation_cache',
                'serial_store':     '/home/billmerrill/topo-cache/b1/serial.no',
                'map_file_dir':     '/home/billmerrill/releases/vcs/topophile/cay',
                'map_file':         '/home/billmerrill/releases/vcs/topophile/cay/prod-srtm-wcs.map',
                'ms_scaling':       True,
                'app_url':          'topophile.com/build/'}
              

local_app_config = {
                'env':      DEV,
                'elevation_server': 'http://127.0.0.1/cgi-bin/mapserv?',
                'model_home_url':   'http://127.0.0.1:9999/',
                'model_dir':        os.path.join(os.getcwd(), "apptest/model_cache"),
                'elevation_dir':    os.path.join(os.getcwd(), "apptest/elevation_cache"),
                'serial_store':     os.path.join(os.getcwd(), "apptest/serial.no"),
                'map_file_dir':     '/Library/WebServer/Documents/cay/',
                'map_file':         '/Library/WebServer/Documents/cay/new-srtm-wcs.map',
                'ms_scaling':       True,
                'app_url':          'topophile.com/build/'}
              