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
            name = sr.record[5].replace(' ', '_')
            ed.save('states/state_{}'.format(name))
            print("{}: {}".format(index, name))


d = Divider("cb_2015_us_state_500k")
d.process_records()
