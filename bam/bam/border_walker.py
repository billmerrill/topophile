import copy

X = 0
Y = 1

class RingGraphNode(object):

    def __init__(self, data):
        self.coord = data
        self.next = None

    def __str__(self):
        return "px{}".format(self.coord)


class RingGraphPath(object):

    BORDER = 255

    LIVE = 'live'
    DEAD = 'dead'

    def __init__(self, origin, grid, history=None):
        origin_node = RingGraphNode(origin)
        grid[origin_node.coord[Y]][origin_node.coord[X]] = 128
        if history:
            # print 'new path history length ', len(history), ' origin ', origin
            self.root = copy.copy(history.root)
            self.curr = self.root
            ptr = history.root.next
            while ptr:
                self.curr.next = copy.copy(ptr)
                self.curr = self.curr.next
                ptr = ptr.next
            self.curr.next = origin_node
            self.curr = self.curr.next
        else:
            # print 'new path no history'
            self.root = origin_node
            self.curr = self.root

        self.state = self.LIVE
        self.grid = grid

    def __len__(self):
        l = 0
        ptr = self.root
        while ptr:
            l += 1
            ptr = ptr.next
        return l

    def add_pixel(self, new_pixel):
        self.grid[new_pixel[Y]][new_pixel[X]] = 128
        self.curr.next = RingGraphNode(new_pixel)
        self.curr = self.curr.next

    def find_next_pixels(self):
        nexts = []
        border_pixels = [[-1, -1], [0, -1], [1, -1], [-1, 0],
                         [1, 0], [-1, 1], [0, 1], [1, 1]]
        for bp in border_pixels:
            # inspect pixel
            ip = [self.curr.coord[X] + bp[X], self.curr.coord[Y] + bp[Y]]
            # if self.grid[ip[Y]][ip[X]] == self.BORDER:
            if self.grid[ip[Y]][ip[X]] != 0:
                nexts.append(ip[:])

        return nexts

    def visited_pixel(self, coord):
        ptr = self.root

        while ptr:
            if ptr.coord == coord:
                return True
            ptr = ptr.next
        return False

    def remove_visited_pixels(self, pixels):
        new_pixels = []
        for p in pixels:
            if not self.visited_pixel(p):
                new_pixels.append(p)
        return new_pixels

    def next_step(self):
        '''
        look outward for more pixels.
        ignore the previous pixel so we don't go backwards
        continue this path on one pixel
        spawn new paths for additional pixels
        '''
        next_pixels = self.find_next_pixels()
        # print 'starting with {} pixels'.format(len(next_pixels))
        next_pixels = self.remove_visited_pixels(next_pixels)
        print 'ending with {} pixels'.format(len(next_pixels))
        print next_pixels

        if next_pixels:
            self.add_pixel(next_pixels.pop(0))
        else:
            self.state = self.DEAD

        return [RingGraphPath(px, self.grid, history=self) for px in next_pixels]

    def is_live(self):
        return self.state == self.LIVE

    def __str__(self):
        o = []
        ptr = self.root
        while ptr:
            o.append(str(ptr.coord))
            ptr = ptr.next

        return "\n".join(o)


class RingGraphGenerator(object):

    BORDER = 255

    def __init__(self, border_raster, border_value=None):
        self.input_raster = border_raster
        if border_value:
            self.BORDER = border_value
        self.grid = self.input_raster.ReadAsArray()
        self.paths = []

    def find_first_pixel(self):
        px = False
        for i in range(self.input_raster.RasterYSize):
            for j in range(self.input_raster.RasterXSize):
                if self.grid[i][j] == self.BORDER:
                    px = [j, i]
                    return px

    def live_paths(self):
        l = 0
        d = 0
        for p in self.paths:
            if p.is_live():
                l += 1
            else:
                d += 1
        print 'path count live:{}  dead:{}'.format(l, d)
        return l > 0


    def tick(self):
        print 'tick'
        tick_paths = []
        for p in self.paths:
            if p.is_live():
                tick_paths.extend(p.next_step())

        return tick_paths

    def create_new_path(self, pixel):
        self.paths.append(RingGraphPath(origin=pixel, grid=self.grid))

    def process_grid(self):
        print "Starting"
        pixel = self.find_first_pixel()
        print "first pixel ", pixel
        self.create_new_path(pixel)
        count = 1
        while self.live_paths():
            new_paths = self.tick()
            self.paths.extend(new_paths)
            count += 1
            if count > 40:
                break

        self.grid[0][0] = 100

        print "Grid Complete"
        print len(self.paths), " paths"
        for i, p in enumerate(self.paths):
            print "Path {}".format(i)
            print p

        return self.paths
