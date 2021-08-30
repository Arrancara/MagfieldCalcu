import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from rectangle import Rectangle
from shapes import Ellipse, Rectangle, Path
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse as Ell


class FileParser:
    def __init__(self):
        pass

    def svgparser(self, filepath):
        """User needs to input the filepath as the SVG file path."""
        # Array containing a list of object names
        extracted_object_types = []
        # Array containing objects themselves
        extracted_objects = []
        # Parse the xml file from the specified path
        tree = ET.parse(filepath)
        # Get the root node of the tree
        root = tree.getroot()

        for child in root:
            if child.tag == "{http://www.w3.org/2000/svg}g":
                g = child

        for x in g:
            extracted_object_types.append(x.tag[28:])
            extracted_objects.append(x.attrib)

        shape_list = []
        for index, obj in enumerate(extracted_objects):
            if extracted_object_types[index] == 'circle' or extracted_object_types[index] == 'ellipse':
                shape_list.append(Ellipse(x=obj['cx'], y=obj['cy'], rx=obj['rx'], ry=obj['ry']))
                shape_list[-1].parametric('t', 0)

            if extracted_object_types[index] == 'rect':
                shape_list.append(Rectangle(x=obj['x'], y=obj['y'], width=obj['width'], height=obj['height']))
                shape_list[-1].parametric('t', 0)

            if extracted_object_types[index] == 'path':
                shape_list.append(Path(obj['d']))
                shape_list[-1].parse_path()
                shape_list[-1].parametric('t', 0)

        return shape_list


if __name__ == "__main__":
    parse = FileParser()
    filepath = r'C:\Users\Adam\Documents\Git\MagfieldCalcu\temp.svg'
    shapes = parse.svgparser(filepath)
    for s in shapes:
        print(s.ell)
