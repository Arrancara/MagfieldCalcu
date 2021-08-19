import pandas as pd
import numpy as np

class FileParser:
    def __init__(self):
        pass

    def parsingfunction(filepath):
        """Function requires the path to the excel file that is generated from above function"""
        df = pd.read_excel(filepath)
        number_of_rows = (df.shape[0])
        #   col = df.radius
        #   p = (df.shape[1])
        angle = []
        line_loc = []
        radius = []
        ox = []
        oy = []
        k = []
        height = []
        x1 = []
        x2 = []
        y1 = []
        y2 = []
        currentline = []
        currentcircle = []
        for index in range(df.shape[0]):
            value = df.iloc[index, 4]
            print(index)
            if value > 0:
                height.append(df.iloc[index, 8])
                radius.append(df.iloc[index, 4])
                ox.append(df.iloc[index, 5])
                oy.append(df.iloc[index, 6])
                angle.append(df.iloc[index, 7])
                # The variable known as "k" is a prefactor that is used within the equation to adjust for the angular
                # displacement of the arc, so i.e. for a full circle k = 1, this is done to ensure that the limits of integration
                # are the same.
                k.append(2 * np.pi / (df.iloc[index, 7]))
                currentcircle.append(df.iloc[index, 9])
            else:
                line_loc.append(index)

        for index in range(len(line_loc)):
            x1.append(df.iloc[(line_loc[index] - 1), 0])
            y1.append(df.iloc[(line_loc[index] - 1), 1])
            x2.append(df.iloc[(line_loc[index] - 1), 2])
            y2.append(df.iloc[(line_loc[index] - 1), 3])
            currentline.append(df.iloc[(line_loc[index] - 1), 9])
        return df, x1, x2, y1, y2, ox, oy, angle, k, currentline, height, radius, currentcircle


    def svgparser(filepath, newfilepath):
        """User needs to input the filepath as the SVG file path. The new file path is where the user wants the EXCEL file"""
        import xml.etree.ElementTree as ET
        import numpy as np
        from rectangle import Rectangle
        from circle import Circle
        from Arc import Arc
        from openpyxl import load_workbook
        Xo1 = []
        Yo1 = []
        Xo2 = []
        Yo2 = []
        radius1 = []
        angle1 = []
        oox = []
        ooy = []
        import re
        # Array containing a list of object names
        extracted_object_types = []
        # Array containing objects themselves
        extracted_objects = []
        # Parse the xaml file from the specified path
        tree = ET.parse(filepath)
        # Get the root node of the tree
        root = tree.getroot()
        # Iterate through all the leaf nodes of the tree.
        for n in root.iter():
            # Remove the prefix and add the name to the list
            extracted_object_types.append(n.tag[28:])
            # Add the attribute dictionary to the list
            extracted_objects.append(n.attrib)
        for index in range(len(extracted_object_types)):
            # Catch all objects of type 'circle' or 'ellipse' from the list when looping over all entries
            if extracted_object_types[index] == 'circle' or extracted_object_types[index] == 'ellipse':
                shape = Circle(x=extracted_objects[index]['cx'], y=extracted_objects[index]['cy'],
                               radius=(extracted_objects[index]['rx']))

                # Appends the extracted data to an array
                oox.append(float((shape.x)))
                ooy.append(float(shape.y))
                radius1.append(float((shape.radius)))
                angle1.append(2 * np.pi)
            # Catch all the objects of type 'rect'

            if extracted_object_types[index] == 'rect':
                shape = Rectangle(x=extracted_objects[index]['x'],
                                  y=extracted_objects[index]['y'],
                                  width=extracted_objects[index]['width'],
                                  height=extracted_objects[index]['height'])
                # Calculate the coordinates of the points and append to a list.
                px1 = float(shape.x)
                py1 = (float(shape.height) + float(shape.y))
                px2 = float(shape.x)
                py2 = float(shape.y)
                px3 = float(shape.x) + float(shape.width)
                py3 = float(shape.y)
                px4 = float(shape.x) + float(shape.width)
                py4 = float(shape.y) + float(shape.height)
                Xo1.append(px1)
                Yo1.append(py1)
                Xo2.append(px2)
                Yo2.append(py2)
                Xo1.append(px2)
                Yo1.append(py2)
                Xo2.append(px3)
                Yo2.append(py3)
                Xo1.append(px3)
                Yo1.append(py3)
                Xo2.append(px4)
                Yo2.append(py4)
                Xo1.append(px4)
                Yo1.append(py4)
                Xo2.append(px1)
                Yo2.append(py4)
                # Manually appends the coordinates of the trail formed by the rectangle.
            if extracted_object_types[index] == 'path':
                # Targets elements that have the object type of 'path'
                temparray1 = re.split(r'([,]+|\'+| +)', str(extracted_objects[index]))
                # Forms a new array that contains splitted data as elements of the array, formed from a singular element of the extracted_objects array
                temparraycheck = str(extracted_objects[index]).split()
                cordinates1 = []

                for j in range(len(temparraycheck)):
                    # Checks for elements called "arc"
                    if temparraycheck[j] == '\'arc\',':
                        # assigns values to the class arc
                        shape = Arc(
                            x=extracted_objects[index]['{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cx'],
                            y=extracted_objects[index]['{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cy'],
                            angleinitial=extracted_objects[index][
                                '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}start'],
                            anglefinal=extracted_objects[index][
                                '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}end'],
                            radius=extracted_objects[index][
                                '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}rx'])
                        # Defines each of the attributes of a class and assigns it specific values that are read from the svg file.
                        oox.append(shape.x.strip('\''))
                        # Removes the quotation marks that come before and after the number before appending it to an array.
                        ooy.append(shape.y)
                        radius1.append(shape.radius)
                        angle1.append((abs(float(shape.angleinitial) - float(shape.anglefinal))))
                        # Appends the angle subtended by the arc by obtaining the difference between the starting and final angle
                        # Appends values to an array, to be used later.
                    else:
                        pass
                if temparraycheck[2] == '\'d\':':
                    # Runs if the array contains 'd' as its third element.
                    for val in temparray1:
                        # Iterates over all the elements within an array to check if each element is a float
                        # All the numerical values are then appended to another array that contains all the coordinates.
                        try:
                            converted_result = float(val)
                            cordinates1.append(converted_result)
                        except ValueError:
                            pass

                    numbers1 = int(len(cordinates1))
                    i = 0
                    for r in range(
                            int((numbers1) / int(
                                2) - 1)):  ## i think we need to just obtain number elements? NOT SURE HOW

                        Xo1.append(cordinates1[i])
                        Yo1.append(cordinates1[i + 1])
                        Xo2.append(cordinates1[i + 2])
                        Yo2.append(cordinates1[i + 3])
                        i = i + 2
                    if len(cordinates1) > 5:  # if there are more than 2 points then we have an additional point that joins the two together.=m
                        Xo1.append(cordinates1[numbers1 - 2])
                        Yo1.append(cordinates1[numbers1 - 1])
                        Xo2.append(cordinates1[0])
                        Yo2.append(cordinates1[1])

        headers = ['x1', 'y1', 'x2', 'y2', 'radius', 'Origin_x', 'Origin_y', 'Angle', 'Height', 'Current']
        workbook_name = newfilepath
        wb = load_workbook(filename=workbook_name)
        page = wb.active
        page.append(headers)
        i = 0
        for i in range(len(Xo1)):
            row = [(Xo1[i]), (Yo1[i]), (Xo2[i]), Yo2[i], 0, 0, 0, 0, 0, 1]
            page.append(row)
            i = i + 1
        i = 0
        # Only runs if there is a circular shape
        if len(radius1) > 0:
            for index in range(len(radius1)):
                row = [0, 0, 0, 0, radius1[i], oox[i], ooy[i], angle1[i],
                       0, 1]
                # The height and current needs to be changed manually by the user
                page.append(row)
                # Add the rows to the excel file
                i = i + 1
        return wb.save(filename=workbook_name)  # Saves the Workbook.


if __name__ == "__main__":
    parse = parser()
    parse.parsingfunction(r'C:\Users\aavas\PycharmProjects\pythonProject1\Line Testing.xlsx')
