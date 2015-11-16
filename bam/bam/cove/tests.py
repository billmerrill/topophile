import unittest

import numpy as np

from mesh import Mesh


class CoveVRMLTests(unittest.TestCase):

    def test_elevation_grid(self):
        input = np.ones((80, 80))
        m = Mesh()
        m.load_matrix(input)
        s = m.get_vrml()
        self.assertEqual(len(s), 25715)


if __name__ == '__main__':
    unittest.main()
