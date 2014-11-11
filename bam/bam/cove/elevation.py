import math
import struct
import gdal
import gdalconst
import osr
import pprint
from haversine import haversine
from indicies import *

class Elevation(object):

    def __init__(self, config):
        self.builder = config
        
    def load_dataset(self):
        self.dataset = gdal.Open(self.builder.get_src_filename(), gdal.GA_ReadOnly)
       
    def close_dataset(self):
       self.dataset = None
            
    def get_longest_raster_size(self):
        return max(self.dataset.RasterXSize, self.dataset.RasterYSize)
        
    def reproject_and_resample(self):
        '''
            Reproject the source data to the target projection
            Then resample the data for the target resolution
        
            Config from builder:
            get_output_projection() - the target epsg
            get_output_resolution() - the number of points on the longest side
            
        '''
        
        # define the size of the input dataset
        input_xform = self.dataset.GetGeoTransform()
        input_geobounds = (input_xform[0], 
                       input_xform[3], 
                       input_xform[0] + (input_xform[1] * self.dataset.RasterXSize), 
                       input_xform[3] + (input_xform[5] * self.dataset.RasterYSize))

        # set up the transform, find the output bounds of the transformed data
        target_proj = osr.SpatialReference()
        target_proj.ImportFromEPSG(self.builder.get_output_projection())
        src_proj = osr.SpatialReference()
        src_proj.ImportFromWkt(self.dataset.GetProjection())
        xform = osr.CoordinateTransformation(src_proj, target_proj)
        (ulx, uly, ulz ) = xform.TransformPoint(input_geobounds[BULX], input_geobounds[BULY])
        (lrx, lry, lrz ) = xform.TransformPoint(input_geobounds[BLRX], input_geobounds[BLRY])
        output_geobounds = (ulx, uly, lrx, lry) 
       
        # define the size of the output dataset
        (output_x_size, output_y_size) = self._get_resampled_raster_size(output_geobounds)
        
        output_pixel_spacing = ( ((output_geobounds[BLRX] - output_geobounds[BULX]) / 
                                   output_x_size),
                                 (-(output_geobounds[BULY] - output_geobounds[BLRY]) / 
                                   output_y_size))
            
        output_xform = (output_geobounds[BULX], 
                        output_pixel_spacing[PX],
                        input_xform[2],
                        output_geobounds[BULY],
                        input_xform[4],
                        output_pixel_spacing[PY])

        # create and setup a new dataset
        mem_drv = gdal.GetDriverByName('MEM')
        output_dataset = mem_drv.Create('', output_x_size, output_y_size, 
            1, self.dataset.GetRasterBand(1).DataType)
        output_dataset.SetGeoTransform(output_xform)
        output_dataset.SetProjection(target_proj.ExportToWkt())

        res = gdal.ReprojectImage(self.dataset, output_dataset, 
                    src_proj.ExportToWkt(), target_proj.ExportToWkt(), 
                    gdal.GRA_Bilinear)    
                    
        return output_dataset
                    
    def _get_resampled_raster_size(self, output_bounds):
        '''
            Get the x and y sizes of a raster to be generated
            based on the current bounds of the data, and 
            the longest edge's resolution
        '''        
        x_r = y_r = 0
        r_max = self.builder.get_output_resolution()
        x_g = abs(output_bounds[BULX] - output_bounds[BLRX]) 
        y_g = abs(output_bounds[BULY] - output_bounds[BLRY])
        
        if x_g > y_g:
            x_r = r_max
            y_r = x_r * (y_g / x_g)
        else:
            y_r = r_max
            x_r = y_r * (x_g / y_g)
            
        return (int(x_r), int(y_r))
                
    def get_meters_matrix(self):
        scaled_dataset = self.reproject_and_resample()
        arr = scaled_dataset.ReadAsArray()
        geo_xform = scaled_dataset.GetGeoTransform()
        scaled_pixel_meters = (geo_xform[1], geo_xform[5])
        
        elevation_matrix = []
        for i in range(0, scaled_dataset.RasterYSize):
            points = []
            for j in range(0, scaled_dataset.RasterXSize):
                points.append ( [scaled_pixel_meters[PX] * j,
                                 scaled_pixel_meters[PY] * i,
                                 arr[i][j]])
            elevation_matrix.append(points)
        
        dst = None
        return elevation_matrix
        
    
    def display_summary(self):
        print 'Driver: ',self.dataset.GetDriver().ShortName,'/', \
             self.dataset.GetDriver().LongName
        print 'Size is ', self.dataset.RasterXSize,'x', self.dataset.RasterYSize, \
              'x',self.dataset.RasterCount
        print 'Projection is '
        pprint.pprint(self.dataset.GetProjection())

        if True:
            band =self.dataset.GetRasterBand(1)
            print 'Band Type=',gdal.GetDataTypeName(band.DataType)

            min = band.GetMinimum()
            max = band.GetMaximum()
            if min is None or max is None:
                (min,max) = band.ComputeRasterMinMax(1)
            print 'Min=%.3f, Max=%.3f' % (min,max)

            if band.GetOverviewCount() > 0:
                print 'Band has ', band.GetOverviewCount(), ' overviews.'
            else:
                print 'Band has no overviews'

            if not band.GetRasterColorTable() is None:
                print 'Band has a color table with ', \
                band.GetRasterColorTable().GetCount(), ' entries.'
            else:
                print 'Band has no color table'

        geotransform =self.dataset.GetGeoTransform()
        if not geotransform is None:
            print 'Origin = (',geotransform[0], ',',geotransform[3],')'
            print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'

      

        