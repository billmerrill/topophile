import geohash


class LatLon(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def get_geohash(self):
        return geohash.encode(float(self.lat), float(self.lon))


class BoundingBox(object):
    def __init__(self, north, west, south, east):
        self.north = north
        self.west = west
        self.south = south
        self.east = east

    def get_nw_corner(self):
        return LatLon(self.north, self.west)

    def get_se_corner(self):
        return LatLon(self.south, self.east)

    def get_geohash(self):
        return "%s-%s" % (self.get_nw_corner().get_geohash(), self.get_se_corner().get_geohash())

    def __str__(self):
        return "{},{},{},{}".format(self.north, self.west, self.south, self.east)
