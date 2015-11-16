import copy
from model import SolidElevationModel, FourWallsModel
from pprint import pprint


model_config = {'src': 'c236gcce2jb0-c236r2812p84.tif',
                'output_resolution': 200,
                'output_physical_max': 100,
                'z_factor': 1.8,
                'min_model_thickness': [2, 2, 2]
                }

fw_model_config = {
    'dst': '/home/billmerrill/webapps/model_cache/c28gb66h0j84-c294bcjjb021-cube-100-200-1_5.stl',
    'hollow': u'1',
    'output_physical_max': 100,
    'output_resolution': 200,
    'resample_elevation': False,
    'src': '/home/billmerrill/topo-cache/b1/elevation_cache/c28gb66h0j84-c294bcjjb021-100-200.tif',
    'z_factor': 1.5}


local_vrml_model_config = {
    'dst': '/Users/bill/topo/bam/bam/apptest/model_cache/test_output.vrml',
    'hollow': u'1',
    'output_physical_max': 100,
    'output_resolution': 200,
    'resample_elevation': False,
    # 'src': '/Users/bill/topo/bam/bam/apptest/elevation_cache/c28gb66h0j84-c294bcjjb021-100-200.tif',
    'src': '/Users/bill/topo/bam/bam/apptest/elevation_cache/9q9jn4n5b5bn-9q97yf2gzgxb-100-200.tif',
    # 'src': '/Users/bill/topo/bam/bam/apptest/elevation_cache/c22zvjb084b5-c23n7uyn0n0h-100-200.tif',
    'z_factor': 1.5}

local_stl_model_config = copy.deepcopy(local_vrml_model_config)
local_stl_model_config[
    'dst'] = '/Users/bill/topo/bam/bam/apptest/model_cache/test_output.stl'


def solid():
    model = SolidElevationModel(model_config)
    model_data = model.build_stl()
    pprint(model_data)


def stl_test():
    model = FourWallsModel(local_stl_model_config)
    model_data = model.build_stl()
    pprint(model_data)


def vrml_test():
    model = FourWallsModel(local_vrml_model_config)
    model_data = model.build_vrml()
    pprint(model_data)


# main()
# test_hollow()
# solid()
# hollow()
vrml_test()
# stl_test()
