import unittest
from state_maker import StateElevationMaker

class StateTests(unittest.TestCase):

    wa_shp = 'test-data/washington-chain/washington-sample.shp'

    def test_bbox_init(self):
        sem = StateElevationMaker(self.wa_shp)
        self.assertEqual(sem.state_bbox.north, 49.003962889899185)
        self.assertEqual(sem.state_bbox.west, -124.73317399999999)
        self.assertEqual(sem.state_bbox.south, 45.543541)
        self.assertEqual(sem.state_bbox.east, -116.915989)


if __name__ == '__main__':
    unittest.main()
