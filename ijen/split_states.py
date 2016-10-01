import shapefile

class StateEditor(shapefile.Editor):

    def __init__(self, filename):
        super(StateEditor, self).__init__(filename)


    def select_state(self, index):
        self._shapes = [self._shapes[index]]
        self.records = [self.records[index]]


class Divider():

    def __init__(self, filename):
        self.filename = filename
        self.reader = shapefile.Reader(filename)
        self.shape_records = self.reader.shapeRecords()

    def process_records(self):
        for index, sr in enumerate(self.shape_records):
            ed = StateEditor(self.filename)
            ed.select_state(index)
            ed.save('states/state_{}'.format(sr.record[5]))
            print sr.record[5]


# ed = StateEditor("cb_2015_us_state_500k")
d = Divider("cb_2015_us_state_500k")
d.process_records()
# ed = shapefile.Editor("cb_2015_state_500k")
# ed.select_state(1)
# ed.save("states/test_ed")

# class StateMaker(object):
#
#     def __init__(self, state_index=0):
#         self.states = shapefile.Reader("cb_2015_state_500k")
#         self.state_index = state_index
#         self.state_shape = self.states.shape(state_index)
#         self.state_record = self.states.record(state_index)
#         self.writer = shapefile.Writer()
#
#     def write_state(self, filename):
#         self.writer.save(filename)
#
#     def copy_shape(self):
#         pass
#
#     def copy_record(self):
#         writer.record(*self.state_record)
#         pass
#
#     def copy_fields(self):
#         fields = self.states.fields
#         for f in fields:
            # writer.field(**f)
