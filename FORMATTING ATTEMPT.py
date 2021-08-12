import numpy as np
import sympy as smp
import pandas as pd
import plotly.graph_objects as go
from IPython.display import HTML
from IPython.display import display
from scipy.integrate import quad
from sympy.interactive import printing
printing.init_printing(use_latex= True) #Prints results in latex format

t,x,y,z = smp.symbols('t x y z')
r = smp.Matrix([x,y,z]) #position vector of an arbitrary point
global mu
mu = float(1.25663706 * 10 ** (-6));

def parsingfunction(filepath):
    df = pd.read_excel(filepath)
    number_of_rows = (df.shape[0])
#   col = df.radius
#   p = (df.shape[1]);
    global angle
    angle = []
    global line_loc
    line_loc = []
    global radius
    radius = []
    global ox
    ox = []
    global oy
    oy = []
    global k
    k = []
    global height
    height = []
    global x1
    x1 = []
    global x2
    x2 =[]
    global y1
    y1 = []
    global y2
    y2 = []
    global currentline
    currentline = []
    global currentcircle
    currentcircle = []
    for index in range(df.shape[0]):
        value = df.iloc[index, 4]
        print(index)
        if value > 0:
            height.append(df.iloc[index, 8])
            radius.append(df.iloc[index,4])
            ox.append(df.iloc[index,5])
            oy.append(df.iloc[index,6])
            angle.append(df.iloc[index,7])
            k.append(2 * np.pi / (df.iloc[index,7]))
            currentcircle.append(df.iloc[index, 9])
        else:
            line_loc.append(index)

    for index in range(len(line_loc)):
        x1.append(df.iloc[(line_loc[index] - 1), 0])
        y1.append(df.iloc[(line_loc[index] - 1), 1])
        x2.append(df.iloc[(line_loc[index] - 1), 2])
        y2.append(df.iloc[(line_loc[index] - 1), 3])
        currentline.append(df.iloc[(line_loc[index] - 1), 9])
    display(df)
    return df,x1,x2,y1,y2,ox,oy,angle,k,currentline,height,radius,currentcircle

parsingfunction(r'C:\Users\aavas\PycharmProjects\pythonProject1\Line Testing.xlsx')

#User needs to input the filepath as the SVG file path. The new file path is where the user wants the EXCEL file.
def svgparser(filepath,newfilepath):
    import xml.etree.ElementTree as ET
    import numpy as np
    from rectangle import Rectangle
    from circle import Circle
    from Arc import Arc
    from openpyxl import load_workbook
    Xo1 = [];
    Yo1 = [];
    Xo2 = [];
    Yo2 = [];
    radius1 = [];
    angle1 = [];
    oox = [];
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
            oox.append(float((shape.x)));
            ooy.append(float(shape.y));
            radius1.append(float((shape.radius)))
            angle1.append(2 * np.pi)
        # Catch all the objects of type 'rect'

        if extracted_object_types[index] == 'rect':
            shape = Rectangle(x=extracted_objects[index]['x'],
                              y=extracted_objects[index]['y'],
                              width=extracted_objects[index]['width'],
                              height=extracted_objects[index]['height'])
            #Calculate the cordinates of the points and append to a list.
            px1 = float(shape.x);
            py1 = (float(shape.height) + float(shape.y));
            px2 = float(shape.x);
            py2 = float(shape.y);
            px3 = float(shape.x) + float(shape.width);
            py3 = float(shape.y);
            px4 = float(shape.x) + float(shape.width);
            py4 = float(shape.y) + float(shape.height)
            Xo1.append(px1);
            Yo1.append(py1);
            Xo2.append(px2);
            Yo2.append(py2);
            Xo1.append(px2);
            Yo1.append(py2);
            Xo2.append(px3);
            Yo2.append(py3)
            Xo1.append(px3);
            Yo1.append(py3);
            Xo2.append(px4);
            Yo2.append(py4);
            Xo1.append(px4);
            Yo1.append(py4);
            Xo2.append(px1);
            Yo2.append(py4)
            #Manually appends the coordinates of the trail formed by the rectangle.
        if extracted_object_types[index] == 'path':
            #Targets elements that have the object type of 'path'
            temparray1 = re.split(r'([,]+|\'+| +)', str(extracted_objects[index]))
            #Forms a new array that contains splitted data as elements of the array, formed from a singular element of the extracted_objects array
            temparraycheck = str(extracted_objects[index]).split()
            cordinates1 = []

            for j in range(len(temparraycheck)):
                #Checks for elements called "arc"
                if temparraycheck[j] == '\'arc\',':
                    #assigns values to the class arc
                    shape = Arc(x=extracted_objects[index]['{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cx'],
                                y=extracted_objects[index]['{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cy'],
                                angleinitial=extracted_objects[index][
                                    '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}start'],
                                anglefinal=extracted_objects[index][
                                    '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}end'],
                                radius=extracted_objects[index][
                                    '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}rx'])
                    #Defines each of the attributes of a class and assigns it specific values that are read from the svg file.
                    oox.append(shape.x.strip('\''))
                    #Removes the quotation marks that come before and after the number before appending it to an array.
                    ooy.append(shape.y)
                    radius1.append(shape.radius)
                    angle1.append((abs(float(shape.angleinitial) - float(shape.anglefinal))))
                    #Appends the angle subtended by the arc by obtaining the difference between the starting and final angle
                    #Appends values to an array, to be used later.
                else:
                    pass
            if temparraycheck[2] == '\'d\':':
                #Runs if the array contains 'd' as its third element.
                for val in temparray1:
                #Iterates over all the elements within an array to check if each element is a float
                #All the numerical values are then appended to another array that contains all the coordinates.
                    try:
                        converted_result = float(val)
                        cordinates1.append(converted_result)
                    except ValueError:
                        pass

                numbers1 = int(len(cordinates1))
                i = 0
                for r in range(
                        int((numbers1) / int(2) - 1)):  ## i think we need to just obtain number elements? NOT SURE HOW

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

    headers = ['x1', 'y1', 'x2', 'y2', 'radius', 'Origin_x', 'Origin_y', 'Angle', 'Height','Current']
    workbook_name = newfilepath
    wb = load_workbook(filename=workbook_name)
    page = wb.active
    page.append(headers)
    i = 0
    for i in range(len(Xo1)):
        row = [(Xo1[i]), (Yo1[i]), (Xo2[i]), Yo2[i], 0, 0, 0, 0, 0,1]
        page.append(row)
        i = i + 1
    i = 0
    #Only runs if there is a circular shape
    if len(radius1) > 0:
        for index in range(len(radius1)):
            row = [0, 0, 0, 0, radius1[i], oox[i], ooy[i], angle1[i],
                   0,1]
            #The height and current needs to be changed manually by the user
            page.append(row)
            #Add the rows to the excel file
            i = i + 1
    return wb.save(filename=workbook_name) #Saves the Workbook.
#Function requires the path to the excel file that is generated from above function,
def Bintegrand(filepath):
    parsingfunction(filepath)
    global totalintegrandarc
    totalintegrandarc = smp.Matrix([0, 0, 0])
    global totalintegrandline
    totalintegrandline = smp.Matrix([0, 0, 0])
    u = 0
    d_x = [];
    d_y = [];
    for index in range(len(line_loc)):  # we want to sort out the straight lines now.
        d_x.append(int(x2[u] - x1[u]))
        d_y.append(int(y2[u] - y1[u]))
        l = smp.Matrix([(x1[u] + t * (d_x[u])), (y1[u] + (t) * (d_y[u])), 0])
        sep = r-l
        integrand = currentline[u] * ((smp.diff(l, t).cross(sep)) / sep.norm() ** 3)
        u = u + 1
        totalintegrandline = integrand + totalintegrandline

        # lx.append(l[0]); ly.append(l[1]); ly.append(l[2])
    for i in range(len(radius)):
        l = smp.Matrix([smp.cos(k[i] * t) + ox[i], smp.sin(k[i] * t) + oy[i], height[i]])
        sep = r - l
        integrand = (smp.diff(l, t).cross(sep) / sep.norm() ** 3) * currentcircle[i]
        totalintegrandarc = totalintegrandarc + integrand
        i = i + 1
    return totalintegrandline
    print(totalintegrandline,"totalintegrandline")
    return totalintegrandarc
    print(totalintegrandarc,"totalintegrandarc")
Bintegrand(r'C:\Users\aavas\PycharmProjects\pythonProject1\Line Testing.xlsx')
print(totalintegrandarc,totalintegrandarc)
def Bfieldplotter(filepath):
    #Bintegrand function is ued to find the integrand of the path.
    Bintegrand(filepath)
    t, x, y, z = smp.symbols('t x y z')
    r = smp.Matrix([x, y, z])  # position vector of an arbitrary point
    #Converting the symbolic function into a numerical one where values can be subbed in for the variables.
    dBxadt = smp.lambdify([t, x, y, z], totalintegrandarc[0])
    dByadt = smp.lambdify([t, x, y, z], totalintegrandarc[1])
    dBzadt = smp.lambdify([t, x, y, z], totalintegrandarc[2])
    dBxldt = smp.lambdify([t, x, y, z], totalintegrandline[0])
    dByldt = smp.lambdify([t, x, y, z], totalintegrandline[1])
    dBzldt = smp.lambdify([t, x, y, z], totalintegrandline[2])

    #Function defined that is used to calculate the B-field at a certian point..
    def B(x, y, z):
        return np.array(([(quad(dBxldt, 0, 1, args=(x, y, z))[0] + quad(dBxadt, 0, 2 * np.pi, args=(x, y, z))[0]),
                          (quad(dByldt, 0, 1, args=(x, y, z))[0] + quad(dByadt, 0, 2 * np.pi, args=(x, y, z))[0]),
                          (quad(dBzldt, 0, 1, args=(x, y, z))[0] + quad(dBzadt, 0, 2 * np.pi, args=(x, y, z))[0])]))
    #Change the array of x, to change where the scatter plot is plotted around
    x = np.linspace(-2, 2, 20)  # creates an array of points

    xv, yv, zv = np.meshgrid(x, x, x)
    # converts the signuature of the file into something that we can feed through to plotly
    B_field = np.vectorize(B, signature='(),(),()->(n)')(xv, yv,
                                                         zv)
    Bx = B_field[:, :, :, 0]
    By = B_field[:, :, :, 1]
    Bz = B_field[:, :, :, 2]

    data = go.Cone(x=xv.ravel(), y=yv.ravel(), z=zv.ravel(),
                   u=Bx.ravel(), v=By.ravel(), w=Bz.ravel(),
                   colorscale='Inferno', colorbar=dict(title='$x^2$'),
                   sizemode="absolute")
    #Defining the title, and the axis lables.
    layout = go.Layout(title=r'B-field',
                       scene=dict(xaxis_title=r'x',
                                  yaxis_title=r'y',
                                  zaxis_title=r'z',
                                  aspectratio=dict(x=1, y=1, z=1),
                                  camera_eye=dict(x=1.2, y=1.2, z=1.2)))
    fig = go.Figure(data=data, layout_yaxis_range=[-4, 4], layout_xaxis_range=[-4, 4])
    #Defines the range of the axis.
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[-5, 5], ),
            yaxis=dict(nticks=4, range=[-5, 5], ),
            zaxis=dict(nticks=4, range=[-5, 5]), ),
        width=700,
        margin=dict(r=20, l=10, b=10, t=10))
    fig.show()
    HTML(fig.to_html())
Bfieldplotter(r'C:\Users\aavas\PycharmProjects\pythonProject1\Line Testing.xlsx')

def Bfinder(filepath,x_cord,y_cord,z_cord):
    Bintegrand(filepath)
    t, x, y, z = smp.symbols('t x y z')
    r = smp.Matrix([x, y, z])  # position vector of an arbitrary point
    # Converting the symbolic function into a numerical one where values can be subbed in for the variables.
    dBxadt = smp.lambdify([t, x, y, z], totalintegrandarc[0])
    dByadt = smp.lambdify([t, x, y, z], totalintegrandarc[1])
    dBzadt = smp.lambdify([t, x, y, z], totalintegrandarc[2])
    dBxldt = smp.lambdify([t, x, y, z], totalintegrandline[0])
    dByldt = smp.lambdify([t, x, y, z], totalintegrandline[1])
    dBzldt = smp.lambdify([t, x, y, z], totalintegrandline[2])

    # Function defined that is used to calculate the B-field at a certian point..
    def B(x, y, z):
        return np.array(([(quad(dBxldt, 0, 1, args=(x, y, z))[0] + quad(dBxadt, 0, 2 * np.pi, args=(x, y, z))[0]),
                          (quad(dByldt, 0, 1, args=(x, y, z))[0] + quad(dByadt, 0, 2 * np.pi, args=(x, y, z))[0]),
                          (quad(dBzldt, 0, 1, args=(x, y, z))[0] + quad(dBzadt, 0, 2 * np.pi, args=(x, y, z))[0])]))
    print(B(x_cord, y_cord, z_cord))
Bfinder(r'C:\Users\aavas\PycharmProjects\pythonProject1\Line Testing.xlsx',1,2,3)

#Blineoptimise finds the minimum length of a line to find a desired B-field at a point.
def Blineoptimise(desiredB,pointofeval_x,pointofeval_y,pointofeval_z):
    t, x, y, z, a, b, c, d = smp.symbols('t x y z a b c d');
    r = smp.Matrix([x, y, z])
    # lets just say we already have a set of points to take the values from, i.e for a unit square with a vertex at 0,0
    current = 100000.00;
    N = 100.00
    x1 = [0]
    y1 = [0]
    x2 = [c]
    y2 = [d]  # we let a = 0, b = 0 so that the statrtingpoint is always the origin, makes computation quicker

    # finding the length of wire that we need to have a desired B-field at a certain point.
    desired_B = desiredB
    l = smp.Matrix([(a + t * ((c - a))), (b + (t) * (d - b)), 0])
    print(l)
    sep = r - l
    integrand = ((smp.diff(l, t)).cross(sep)) / (sep.norm() ** 3)
    mu = float(1.25663706 * 10 ** (-6));
    constant = float(mu * current * N / (4 * np.pi))
    #Subbing in initial value.
    integrandoptimise = integrand.subs(

        {a: x1[0], b: y1[0], x: pointofeval_x, y: pointofeval_y, z: pointofeval_z})
    return integrand

    for index in range(3):
        integrandoptimise[index] = constant * integrandoptimise[index]
        integrand[index] = constant * integrand[index]
    dBoptmisex = smp.lambdify(([t, c, d]), integrandoptimise[0])
    dBoptmisey = smp.lambdify(([t, c, d]), integrandoptimise[1])
    dBoptmisez = smp.lambdify(([t, c, d]), integrandoptimise[2])

    def Boptimise(c, d):
        return np.array([quad(dBoptmisex, 0, 1, args=(c, d))[0],
                         quad(dBoptmisey, 0, 1, args=(c, d))[0],
                         quad(dBoptmisez, 0, 1, args=(c, d))[0]])
    #The user can change the accuracy of the optimiser by changing the number of data points
    #ThE user can also change the boundaries for c and d for the optimiser.
    d = np.linspace(0, 1, 100)
    c = np.linspace(0, 1, 100)
    stored_B_array = []
    for index in range(c.size):
        arr = []
        for count in range(d.size):
            val = np.linalg.norm(Boptimise(c[index], d[count]))
            arr.append(val)
        stored_B_array.append(arr)
    print(stored_B_array[0][1])
    column_index = [];
    min_values = []

    for index in range(c.size):
        row_array = np.array(stored_B_array[index])
        idx = np.abs(row_array - desired_B).argmin()
        min_values.append(row_array[idx])
        column_index.append(idx)
        row_array = np.append(row_array, stored_B_array[index][idx])

    idx = np.abs(np.abs(np.asarray(min_values) - desired_B)).argmin()
    d_val = column_index[idx]
    optimised_c = c[idx];
    optimised_d = d[d_val]
    return print(" c= ", "{:e}".format(c[idx]), "d =", "{:e}".format(d[d_val]))
    return c[idx]
    return d[d_val]
Blineoptimise(1,1,1,1)
#Function to optimise the B-field due to a circle centered at (ox,oy), the point of evaluation must be inputted.
#Can add an angle input for added functionality of allowing for arcs, but it is omitted to reduce the number of inputs
#required, as 2*pi would be needed to be inputted for a circle.
def BcircleOptimse(desiredB, center_x,center_y,pointofeval_x,pointofeval_y,pointofeval_z):
    t, x, y, z = smp.symbols('t x y z');
    r = smp.Matrix([x, y, z])

    # User input of the desired B-field at the point, inputted as a float.
    desired_B = float(1)

    desired_B_array = [0, 0,0]  # if you leave it as 0 then we just ignore the specific component, i.e. wont optimise for it.
    number_of_loops = 1  # decide how many loops you want.

    calc_radius = []
    # Point of evaluation of the field.
    point_of_evaluation = [pointofeval_x, pointofeval_y, pointofeval_z]  # where we evaulate the B-field

    ## we are going to define R = position vector of the line, dl = line element along the line

    ##we are trying to solve the B-field at a point in space, and then try to obtain the minimum radius of the loop that we need.

    current = float(1.00)  # defining the current of the loop in AMPS.
    ox = center_x
    oy = center_y
    height = [0]  # you can adjust the parameterrs of the coil of loop as you feel necessary.
    mu = float(1.25663706 * 10 ** (-6))
    constant = float(mu / (4 * np.pi))
    totalintegrandarc = smp.Matrix([0, 0, 0])  # this leaves for multiple coil setup as you desire, ignored for now.

    #The total integrand arc is left here for future development where the user can input multiple coils (like a solenoid)
    #and optimise for a solenoid.
    l = smp.Matrix([smp.cos(t) + ox, smp.sin(t) + oy, height[0]])
    sep = r - l
    integrand = (smp.diff(l, t).cross(sep) / sep.norm() ** 3) * current
    totalintegrandarc = totalintegrandarc + integrand
    for con in range(3):
        totalintegrandarc[con] = constant * totalintegrandarc[con]
    dBxadt = smp.lambdify([t, x, y, z], totalintegrandarc[0])
    dByadt = smp.lambdify([t, x, y, z], totalintegrandarc[1])
    dBzadt = smp.lambdify([t, x, y, z], totalintegrandarc[2])

    def B(x, y, z):
        return np.array(([(quad(dBxadt, 0, 2 * np.pi, args=(x, y, z))[0]),
                          (quad(dByadt, 0, 2 * np.pi, args=(x, y, z))[0]),
                          (quad(dBzadt, 0, 2 * np.pi, args=(x, y, z))[0])]))

    stored_B = B(point_of_evaluation[0], point_of_evaluation[1], point_of_evaluation[2])
    temp_rad = []
    # for index in range(3):
    #     # we will check every component of the B-field
    #     if desired_B_array[index] == 0:
    #         pass
    #     else:
    #         temp_rad.append(desired_B_array[index] / stored_B[index])
    # projectedB = []
    # projectedB.append(temp_rad[0] * stored_B[0])
    # projectedB.append(temp_rad[0] * stored_B[1])
    # projectedB.append(temp_rad[0] * stored_B[2])
    # print('The expected B-field is given current setup: ', stored_B)
    # print('Optimising as given leads us to: ', projectedB)
    # print(projectedB)
    B_field = np.linalg.norm(B(point_of_evaluation[0], point_of_evaluation[1], point_of_evaluation[2]))
    calc_radius.append(desired_B / B_field)
    print('The necessary radius is: ', calc_radius)
    return calc_radius
BcircleOptimse(1,0,0,1,1,1)

#This requires the user to input a function in cartesian coordinates in vector form,
#this will be used to define "l", there is a limit to how the functions an be inputted, it must be parameterised
#using the letter "t" as the integrating function.



# def Bfieldfunction(function_x,function_y,function_z):
#     t, x, y, z = smp.symbols('t x y z')
#     r = smp.Matrix([x, y, z])
#     l = smp.Matrix[function_x,function_y,function_z]
#     sep = r-l
#     integrand =(smp.diff(l, t).cross(sep)) / sep.norm() ** 3
#
#     N = 1
#     current = 1
#
#     constant = float(mu * current * N / (4 * np.pi))
#
#     for con in range(3):
#         integrand[con] = constant * integrand[con]
#     dBxdt = smp.lambdify([t, x, y, z], integrand[0])
#     dBydt = smp.lambdify([t, x, y, z], integrand[1])
#     dBzdt = smp.lambdify([t, x, y, z], integrand[2])
#
#     def B(x, y, z):
#
#         return np.array(([(quad(dBxdt, 0, 2 * np.pi, args=(x, y, z))[0]),
#                           (quad(dBydt, 0, 2 * np.pi, args=(x, y, z))[0]),
#                           (quad(dBzdt, 0, 2 * np.pi, args=(x, y, z))[0])]))
#     def l(aux):
#         return np.array([function_x,function_y,function_z])
#     l_x,l_y,l_z = l(aux)
#     x = np.linspace(-2, 2, 20)  # creates an array of points
#     xv, yv, zv = np.meshgrid(x, x, x)
#     B_field = np.vectorize(B, signature='(),(),()->(n)')(xv, yv,
#                                                          zv)  # converts the signuature of the file into something that we can feed through to plotly
#     # i.e. converts from 3 distinct numbers to one that we can use for xv,yv,zv.x
#     Bx = B_field[:, :, :, 0]
#     By = B_field[:, :, :, 1]
#     Bz = B_field[:, :, :, 2]
#     # the data is obtained usiing the ravel function which converts the data into an 1-D array that be fed through the file.
#     data = go.Cone(x=xv.ravel(), y=yv.ravel(), z=zv.ravel(),
#                    u=Bx.ravel(), v=By.ravel(), w=Bz.ravel(),
#                    colorscale='Inferno', colorbar=dict(title='$x^2$'),
#                    sizemode="absolute")
#     layout = go.Layout(title=r'B-field',
#                        scene=dict(xaxis_title=r'x',
#                                   yaxis_title=r'y',
#                                   zaxis_title=r'z',
#                                   aspectratio=dict(x=1, y=1, z=1),
#                                   camera_eye=dict(x=1.2, y=1.2, z=1.2)))
#     fig = go.Figure(data=data, layout_yaxis_range=[-4, 4], layout_xaxis_range=[-4, 4])
#     fig.update_layout(
#         scene=dict(
#             xaxis=dict(nticks=4, range=[-5, 5], ),
#             yaxis=dict(nticks=4, range=[-5, 5], ),
#             zaxis=dict(nticks=4, range=[-5, 5]), ),
#         width=700,
#         margin=dict(r=20, l=10, b=10, t=10))
#     fig.add_scatter3d(x=l_x, y=l_y, z=l_y,mode='lines',
#                       line=dict(color='blue', width=10))
#     fig.show()
#     HTML(fig.to_html())
# Bfieldfunction(0,0,t)