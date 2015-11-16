import vrml_templates
import tempfile


class VRMLCanvas(object):

    def __init__(self):
        self.elements = []

    def add_element(self, new_element):
        self.elements.append(new_element)

    def write_vrml(self, outfile):
        print ("Writing %s elements" % len(self.elements))
        with open(outfile, 'wb') as dest_file:
            dest_file.write(vrml_templates.Header)
            for e in self.elements:
                dest_file.write(e.get_vrml())
