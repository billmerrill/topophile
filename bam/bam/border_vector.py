

class BorderSegment(object):

    def __init__(self, initial_pt=None):
        if initial_pt:
            self.pts = [initial_pt]
        else:
            self.pts = []
        self.head = 0
        self.tail = 0

    def add_pt(self, pt, hint=None):
        if self.tail == 0:
            self.add_to_tail(pt)
        elif len(self.pts) == 1:
            self.add_second_point(pt)
        else:
            if self.is_adjacent(self.head, pt):
                self.add_to_head(pt)
            elif self.is_adjacent(self.tail, pt):
                self.add_to_tail(pt)

    def is_pt_adjacent(self, pt):
        if self.tail == 0:
            return True
        return self.is_adjacent(self.head, pt) or self.is_adjacent(self.tail, pt)

    def is_adjacent(self, end, pt):
        if self.tail == 0:
            return True

        end_pt = self.pts[end]
        print "testing is adjacent", end_pt, pt
        return end_pt[0] - 1 <= pt[0] <= end_pt[0] + 1 and \
            end_pt[1] - 1 <= pt[1] <= end_pt[1] + 1

    def is_lead_adjacent(self, end, pt):
        if self.tail == 0:
            return True

        end_pt = self.pts[end]
        return end_pt[0] <= pt[0] <= end_pt[0] + 1 and \
            end_pt[1] - 1 <= pt[1] <= end_pt[1] + 1

    def is_pt_mid_or_trail_adjacent(self, end, pt):
        if self.tail == 0:
            return True

        end_pt = self.pts[end]
        return end_pt[0] - 1 <= pt[0] <= end_pt[0] and \
            end_pt[1] - 1 < pt[1] <= end_pt[1] + 1

    def is_pt_lead_adjacent(self, pt):
        if self.tail == 0:
            return True

        return self.is_lead_adjacent(self.head, pt) or self.is_lead_adjacent(self.tail, pt)

    def is_cluster_mid_or_trail_adjacent(self, cluster, row):
        if self.tail == 0:
            return True

        for pt in cluster:
            if self.is_pt_mid_or_trail_adjacent(self.head, (pt, row)) or \
               self.is_pt_mid_or_trail_adjacent(self.tail, (pt, row)):
                return True
        return False

    def add_second_point(self, pt):
        if pt[0] > self.pts[self.head][0]:
            self.add_to_tail(pt)
        else:
            self.add_to_head(pt)

    def add_to_head(self, pt):
        self.pts.insert(0, pt)

    def add_to_tail(self, pt):
        self.pts.append(pt)
        self.tail = len(self.pts) - 1

    def add_cluster_to_head(self, cluster, row):
        for pt in cluster:
            self.add_to_head((pt, row))

    def add_cluster_to_tail(self, cluster, row):
        for pt in cluster:
            self.add_to_tail((pt, row))

    def add_cluster_if_reverse_adjacent(self, cluster, row):
        for pt in cluster:
            if self.is_adjacent(self.head, (pt, row)):
                self.reverse_add_cluster_to_head(cluster, row)
                return True
            if self.is_adjacent(self.tail, (pt, row)):
                self.reverse_add_cluster_to_tail(cluster, row)
                return True
        return False

    def reverse_add_cluster_to_head(self, cluster, row):
        for index in range(len(cluster) - 1, -1, -1):
            self.add_to_head((cluster[index], row))

    def reverse_add_cluster_to_tail(self, cluster, row):
        for index in range(len(cluster) - 1, -1, -1):
            self.add_to_tail((cluster[index], row))


class BorderVectorSegments(object):

    def __init__(self):
        self.segments = []
        self.segments.append(BorderSegment())

    def start_new_segment_with_cluster(self, cluster, row):
        bs = BorderSegment()
        for pt in cluster:
            bs.add_to_tail((pt, row))
        self.segments.append(bs)

    def add_pt_if_adjacent(self, pt):
        for seg in self.segments:
            if seg.is_pt_adjacent(pt):
                seg.add_pt(pt)
                return True

        return False

    def is_cluster_lead_adjacent(self, cluster, row):
        for index, seg in enumerate(self.segments):
            if seg.is_pt_lead_adjacent((cluster[0], row)):
                return index
        return None

    def is_cluster_mid_or_trail_adjacent(self, cluster, row):
        for index, seg in enumerate(self.segments):
            if seg.is_cluster_mid_or_trail_adjacent(cluster, row):
                return index
        return None

    def add_cluster_to_segment(self, segment, cluster, row, hint='head'):
        if hint == 'tail':
            self.segments[segment].add_cluster_to_tail(cluster, row)
        else:
            self.segments[segment].add_cluster_to_head(cluster, row)

    def add_cluster_if_reverse_adjacent(self, cluster, row):
        for seg in self.segments:
            added = seg.add_cluster_if_reverse_adjacent(cluster, row)
            if added:
                return True
        return False


class BorderVector(object):

    def __init__(self, border_raster, border_value=255):
        self.segments = BorderVectorSegments()
        self.input_raster = border_raster
        self.border_value = border_value
        self.grid = self.input_raster.ReadAsArray()
        self.border_pixel_count = 0

    def generate(self):
        for row_index in range(self.input_raster.RasterYSize):
            print "row ", row_index
            self.process_row(row_index)
            if row_index == 200:
                break

        print 'found pixels', self.border_pixel_count
        tot = 0
        for s in self.segments.segments:
            tot += len(s.pts)
            print 'seg size: ', len(s.pts)

        print "total in segments: ", tot

    def gather_row_clusters(self, row):
        row_clusters = []

        col = 0
        while col < self.input_raster.RasterXSize:
            if self.grid[row][col] == self.border_value:
                cluster = []
                cluster.append(col)
                col += 1
                while col < self.input_raster.RasterXSize and \
                        self.grid[row][col] == self.border_value:
                    cluster.append(col)
                    col += 1
                self.border_pixel_count += len(cluster)
                row_clusters.append(cluster)
            else:
                col += 1

        return row_clusters

    def cluster_first_pass(self, row_clusters, row):
        #  First Pass
        #  Lone Adj Pt get added
        #  Lead Adj Pt Clusters get added in order { initial p(x) >= seg_end_p(x)}
        #  Mid/Trail Adj Pt Clusters get deffered  { initial p(x) < seg_end_px(x)}
        #  optimization, we could track the segments the deferred clusters are adjancent too for less searching in the second.

        deferred = []

        for index, cluster in enumerate(row_clusters):
            if len(cluster) is 1:
                print "adding ", (cluster[0], row)
                added = self.segments.add_pt_if_adjacent((cluster[0], row))
                if not added:
                    deferred.append(cluster)
                continue

            seg_index = self.segments.is_cluster_lead_adjacent(cluster, row)
            if seg_index is not None:
                self.segments.add_cluster_to_segment(seg_index, cluster, row, hint='head')
                continue

            seg_index = self.segments.is_cluster_mid_or_trail_adjacent(cluster, row)
            if seg_index is not None:
                deferred.append(cluster)

        return deferred


    def cluster_second_pass(self, deferred, row):
        #  Second pass
        #  Process in reverse order
        #  Check for adjanceny with the tail of the cluster and append

        for cluster_index in range(len(deferred)-1, -1, -1):
            c = deferred[cluster_index]
            added = self.segments.add_cluster_if_reverse_adjacent(c, row)
            if not added:
                print "Did not find match for deferred", ",".join(map(str, c))
                self.segments.start_new_segment_with_cluster(c, row)
                del(deferred[cluster_index])


    def process_row(self, row):
        row_clusters = self.gather_row_clusters(row)
        print row_clusters
        deferred = []

        #  First Pass
        #  Lone Adj Pt get added
        #  Lead Adj Pt Clusters get added in order { initial p(x) >= seg_end_p(x)}
        #  Mid/Trail Adj Pt Clusters get deffered  { initial p(x) < seg_end_px(x)}
        deferred = self.cluster_first_pass(row_clusters, row)
        self.cluster_second_pass(deferred, row)
