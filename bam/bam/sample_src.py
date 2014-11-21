import os
import random

'''
2166AC10-449E-48DF-99FE-751B7DA45F43.tif - Upper Left  (-121.8530000,  46.8999000) - Lower Right (-121.6838333,  46.8057333)
55F49F2A-4AE8-4CE3-BF71-A4F541DA3074.tif - Upper Left  (  -6.6137700,  36.9762000) - (  -4.5812700,  35.2362000)
AE992AD5-ED2F-491D-A2C9-550B34118779.tif - Upper Left  (   8.1340000,  47.5543000) - Lower Right (   8.6131667,  47.2026333)
D6AF50E3-7EA3-4A7E-B2C2-70E48B218D3D.tif - Upper Left  (-121.8850000,  46.8264000) - Lower Right (-121.6433333,  46.8055667)
E9CE50A9-C44B-4362-BB5E-F437CCBC16A2.tif - Upper Left  (-121.7500000,  46.9859000) - Lower Right (-121.2900000,  46.6642333)
F8C9F218-6125-4410-AA8E-C94745869BBC.tif - Upper Left  (-123.3050000,  47.8095000) - Lower Right (-123.1683333,  47.3795000)
'''

samples = [ #{'filename': '2166AC10-449E-48DF-99FE-751B7DA45F43.tif',
            # 'nwlat': 46.8999000,
             #'nwlon': -121.8530000,
             #'selat': 46.8057333,
             #'selon': -121.6838333},
        #    {'filename': '55F49F2A-4AE8-4CE3-BF71-A4F541DA3074.tif',
         #   'nwlat': 36.9762000,
          #  'nwlon': -6.6137700,
           # 'selat': 35.2362000,
            #'selon': -4.5812700},
            {'filename': 'AE992AD5-ED2F-491D-A2C9-550B34118779.tif',
            'nwlat': 47.5543000,
            'nwlon': 8.1340000,
            'selat': 47.2026333,
            'selon': 8.6131667},
            {'filename': 'D6AF50E3-7EA3-4A7E-B2C2-70E48B218D3D.tif',
            'nwlat': 46.8264000,
            'nwlon': -121.8850000,
            'selat': 46.8055667,
            'selon': -121.6433333},
            {'filename': 'E9CE50A9-C44B-4362-BB5E-F437CCBC16A2.tif',
            'nwlat': 46.9859000,
            'nwlon': -121.7500000,
            'selat': 46.6642333,
            'selon': -121.2900000},
            {'filename': 'F8C9F218-6125-4410-AA8E-C94745869BBC.tif',
            'nwlat': 47.8095000,
            'nwlon': -123.3050000,
            'selat': 47.3795000,
            'selon': -123.1683333},
             ]

def get_elevation(nwlat, nwlon, selat, selon):
    # random.shuffle(samples)
    filename = os.path.join(os.getcwd(), 'sample-elevation', samples[1]['filename'])

    return {'filename': filename ,
            'nwlat': samples[1]['nwlat'],
            'nwlon': samples[1]['nwlon'],
            'selat': samples[1]['selat'],
            'selon': samples[1]['selon']}