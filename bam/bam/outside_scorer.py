import numpy as np

'''
1.
Iterating from 0,0, known to be Outside, find the first border pixel.
The first border pixel is now added to the path, it is the origin for analysis
The pixel before the border pixel is Outside (1 value)

2. Mark the origin as consumed (128)

N. Temporary mark all
2. Mark all non-border pixels (1 value) pixels that are 4-way contiguous
with the Outside pixel as Outside.

3. Score all non-consumed, non-origin border pixels for their 8-way contingousness
with Ouside pixels.

4. Pick the highest scoring pixels as next origin.  pass along neighboring Outside pixel


'''


class RingGraphGenerator(object):

    BORDER = 255
    OUTSIDE = 1
    EMPTY = 0
    CONSUMED = 128


    def __init__(self, border_raster, border_value=None):
        self.input_raster = border_raster
        if border_value:
            self.BORDER = border_value
        self.grid = self.input_raster.ReadAsArray()
        self.work = self.grid.copy()
        self.path = []
        self.k = np.zeros((3,3))

    def find_first_pixel(self):
        pixel = False
        outside
        for i in range(self.input_raster.RasterYSize):
            for j in range(self.input_raster.RasterXSize):
                if self.grid[i][j] == self.BORDER:
                    pixel = [j, i]
                    if j > 0:
                        outside = [j-1, i]
                    else:
                        outside = [j, i-1]

                    return pixel, outside

    def process_grid(self):
        (origin, outside) = self.find_first_pixel()
        self.path = [origin]
        while true:
            (origin, outside) = self.find_next(origin, outside)


    def find_next(self, x, out):
        border_count = self.count_border(x)
        if border_count == 1:
            (new_x, new_outside) = self.simple_next(x,out)
        self.paint_outside(x, out)

    def simple_next(self, x, out):
        work = self.grid[x[Y]-1:x[Y]+2, x[X]-1:x[X]+2]
        for coord, val in np.ndeumerate(work):
            if val == self.BORDER:
                next_px = coord
                break

        next_dir = np.subtract(next_px, x)
        if np.add(out, next_dir)

    def border_count(self, x):
        work = self.grid[x[Y]-1:x[Y]+2, x[X]-1:x[X]+2]
        bc = 0
        for p in np.nditer(work):
            if p == self.BORDER:
                bc += 1

        return bc

    def paint_outside(self, x, out):
        for i in range(3):
            for py in range(x[Y]-1,x[Y]+2):
                for px in range(x[X]-1,x[X]+2):
                    if self.work[py,px] == self.EMPTY and
