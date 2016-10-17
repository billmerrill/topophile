import geohash
from pyproj import Proj, transform

EPSG_3857 = "epsg:3857"
EPSG_4326 = "epsg:4326"


class LatLon(object):
    def __init__(self, lat, lon, srs):
        self.lat = lat
        self.lon = lon
        self.srs = srs
        self.reproj_lat = None
        self.reproj_lon = None

    def reproject(self, in_lat, in_lon, src_srs):
        in_proj = Proj(init=src_srs)
        out_proj = Proj(init='epsg:4326')
        lon,lat = transform(in_proj,out_proj,in_lon,in_lat)
        return (lon, lat)

    def get_geohash(self):
        if self.srs != EPSG_4326:
            if not self.reproj_lat:
                nlon, nlat = self.reproject(self.lat, self.lon, self.srs)
                self.reproj_lat = nlat
                self.reproj_lon = nlon
            return geohash.encode(self.reproj_lat, self.reproj_lon)

        return geohash.encode(float(self.lat), float(self.lon))


class BoundingBox(object):
    def __init__(self, north, west, south, east, srs=EPSG_4326):
        self.north = north
        self.west = west
        self.south = south
        self.east = east
        self.srs = srs

    def get_nw_corner(self):
        return LatLon(self.north, self.west, self.srs)

    def get_se_corner(self):
        return LatLon(self.south, self.east, self.srs)

    def get_geohash(self):
        return "%s-%s" % (self.get_nw_corner().get_geohash(), self.get_se_corner().get_geohash())

    def __str__(self):
        return "{},{},{},{}".format(self.north, self.west, self.south, self.east)
