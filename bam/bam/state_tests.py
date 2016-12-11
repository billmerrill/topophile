import unittest
from state_maker import StateElevationMaker

class StateTests(unittest.TestCase):

    wa_poly_shp = 'test-data/washington-chain/washington-sample-3857.shp'
    wa_line_shp = 'test-data/washington-chain/lines-3857.shp'

    def x_test_bbox_init(self):
        sem = StateElevationMaker(self.wa_poly_shp, self.wa_line_shp)
        self.assertEqual(sem.state_bbox.north, 49.003962889899185)
        self.assertEqual(sem.state_bbox.west, -124.73317399999999)
        self.assertEqual(sem.state_bbox.south, 45.543541)
        self.assertEqual(sem.state_bbox.east, -116.915989)

    def test_bbox_query(self):
        sem = StateElevationMaker(self.wa_poly_shp, self.wa_line_shp)
        sem.query_elevation()
        ring = sem.create_outline()
        ring = [1]
        self.assertTrue(len(ring) > 800, "Ring Length is {}".format(len(ring)))


if __name__ == '__main__':
    unittest.main()
