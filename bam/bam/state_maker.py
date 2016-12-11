import gdal
import ogr
import shapefile

from border_walker import RingGraphGenerator
from border_vector import BorderVector
import geo
import model_ticket
from topoconf import local_app_config as app_config

# Given a state shapefile, get the appropriate elevation DEM

class StateElevationMaker(object):

    def __init__(self, state_polygon_shp, state_line_shp):
        self.state_polygon_shp = state_polygon_shp
        self.state_line_shp = state_line_shp
        self.state_bbox = None
        self.ticket = None
        self.init_state_bbox()
        self._make_ticket()
        self.state_pixel_ring = None

    def init_state_bbox(self):
        reader = shapefile.Reader(self.state_polygon_shp)
        if len(reader.shapes()) > 1:
            raise Exception("Too many shapes in shapefile:", len(reader.shapes()))
        state_shp = reader.shape(0)
        bbox = state_shp.bbox
        print 'state shp bbox', bbox
        #>>> s.bbox
        #[-124.73317399999999, 45.543541, -116.915989, 49.003962889899185]k
        # west south east north
        # state shp bbox [-13 885 233.414708788, 5 707 500.65707957, -13015028.361071974, 6275533.840261462]

        # self.state_bbox = geo.BoundingBox(bbox[3], bbox[0], bbox[1], bbox[2], srs=geo.EPSG_3857)
        self.state_bbox = geo.BoundingBox(bbox[3]+10000, bbox[0]-10000, bbox[1]-10000, bbox[2]+10000, srs=geo.EPSG_3857)
        print "state bbox", self.state_bbox

    def _scale_state_extent_to_rez(self, rez):
        '''
        '''
        width = abs(self.state_bbox.west - self.state_bbox.east)
        height = abs(self.state_bbox.north - self.state_bbox.south)

        if width > height:
            height = rez * (height / width)
            width = rez
        else:
            width = rez * (width / height)
            height = rez
        return (width, height)

    def _make_ticket(self):
        size = 100
        rez = 800
        zfactor = 5.0
        self.ticket = model_ticket.get_ticket(app_config=app_config,
                               style='state-color',
                               bbox=self.state_bbox,
                               size=size,
                               rez=rez,
                               zmult=zfactor,
                               hollow=True)

        # in the web app, the front end controls the resolution, resolution is
        # specified by the rez param, which is really the number of data points on
        # long side (regardless of the physical size, so not really rez.)
        # anyways, here, take the ratio of the state extent sides and scale
        # them to the rez to control the elevation query size
        (width, height) = self._scale_state_extent_to_rez(rez)
        self.ticket.set_elevation_dimensions(int(round(float(width))),
                                       int(round(float(height))))

    def query_elevation(self):
        self.ticket.data.query_statemaker_elevation()

    def array_to_geotiff(matrix, driver,
                  xsize, ysize, GeoT, Projection):
        DataType = gdal.GDT_Int16
        NewFileName = 'chewed-up-border.tif'
        # Set up the dataset
        DataSet = driver.Create( NewFileName, xsize, ysize, 1, DataType )
                # the '1' is for band 1.
        DataSet.SetGeoTransform(GeoT)
        DataSet.SetProjection( Projection.ExportToWkt() )
        # Write the array
        DataSet.GetRasterBand(1).WriteArray( Array )
        return NewFileName

    def create_outline(self):

        # next save elevation to a particular area

        # generate a MEM raster of the lines shapefile at the resolution of the elevation
        elevation_raster = gdal.Open(self.ticket.get_elevation_filepath(), gdal.GA_ReadOnly)
        elevation_band = elevation_raster.GetRasterBand(1)
        elevation_xform = elevation_raster.GetGeoTransform()

        border_vector = ogr.Open(self.state_line_shp)
        bv_layer = border_vector.GetLayer()

        border_raster = gdal.GetDriverByName('GTiff').Create('test-border-output.tif', elevation_band.XSize, elevation_band.YSize, 1, gdal.GDT_Byte)
        # border_raster = gdal.GetDriverByName('MEM').Create('', elevation_band.XSize, elevation_band.YSize, 1, gdal.GDT_Byte)
        border_raster.SetGeoTransform(elevation_xform)
        br_band = border_raster.GetRasterBand(1)
        br_band.SetNoDataValue(0)

        gdal.RasterizeLayer(border_raster, [1], bv_layer, burn_values=[255])


        # write magic to string pixels in the raster to a linearring style descript of pixel/pts
        # brg = BorderRingGenerator(border_raster)
        # ring = brg.build_ring()
        # rgg = RingGraphGenerator(border_raster)
        # ring = rgg.process_grid()
        # print ring
        # print len(ring)
        #

        bv =BorderVector(border_raster)
        bv.generate()

        chewed_border = gdal.GetDriverByName('GTiff').Create('chewed-border.tif', elevation_band.XSize, elevation_band.YSize, 1, gdal.GDT_Byte)
        chewed_border.SetGeoTransform(elevation_xform)
        cb_band = chewed_border.GetRasterBand(1)
        # #
        cb_band.WriteArray(bv.grid)

        # return ring
        # generate elevation punch out
        # start gluing stuff together
