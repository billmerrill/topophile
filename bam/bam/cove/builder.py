from indicies import *


class Builder(object):

    def __init__(self, kwargs):
        self.src_filename = kwargs['src']
        self.dst_filename = kwargs.get('dst', self._default_dst_name())
        self.output_resolution = kwargs.get('output_resolution', 50)  # data points
        self.output_physical_max = kwargs.get('output_physical_max', 200)  # output mm

        self.sample_rate = kwargs.get('sample_rate', 1)
        self.output_size_x = kwargs.get('output_size_x', 200)
        self.resize_ratio = kwargs.get('resize_ratio', (1, 1))
        self.output_projection_epsg = 3857
        self.z_factor = kwargs.get('z_factor', 1.0)
        self.min_model_thickness = kwargs.get('min_model_thickness', [3, 3, 3])  # mm
        self.ceiling_decimation_factor = kwargs.get('ceiling_decimation_factor', [6, 6])
        self.hollow = kwargs.get('hollow', False)
        self.resample_elevation_input = kwargs.get('resample_elevation', False)

    def _default_dst_name(self):
        return self.src_filename.replace(".tif", ".stl")

    def get_src_filename(self):
        return self.src_filename

    def get_input_sample_rate(self):
        return self.sample_rate

    def get_resize_ratio(self, src_longest_size=None):
        if src_longest_size:
            if src_longest_size == self.output_resolution:
                self.resize_ratio = (1, 1)
            else:
                ratio = float(self.output_resolution) / src_longest_size
                self.resize_ratio = (ratio, ratio)

        return self.resize_ratio

    def get_output_file_name(self):
        return self.dst_filename

    def get_physical_max(self):
        return self.output_physical_max

    def get_output_resolution(self):
        return self.output_resolution

    def get_output_projection(self):
        return self.output_projection_epsg

    def get_z_factor(self):
        return self.z_factor

    def get_min_thickness(self):
        # scale z thickness by the vertical exageration
        mt = [self.min_model_thickness[0], self.min_model_thickness[1], 0]
        zt = self.min_model_thickness[2]
        mt[2] = zt + zt * 0.1 * self.z_factor
        return mt

    def get_ceiling_decimation_factor(self):
        return self.ceiling_decimation_factor

    def is_hollow(self):
        return self.hollow

    def get_resample_elevation(self):
        return self.resample_elevation_input
