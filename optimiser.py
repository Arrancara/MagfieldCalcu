
class optimise:
    def __init__(self):
        pass

    def Blineoptimise(desiredB, pointofeval_x, pointofeval_y, pointofeval_z):
        """Blineoptimise finds the minimum length of a line to find a desired B-field at a point."""
        t, x, y, z, a, b, c, d = smp.symbols('t x y z a b c d')
        r = smp.Matrix([x, y, z])
        # lets just say we already have a set of points to take the values from, i.e for a unit square with a vertex at 0,0
        current = 100000.00
        N = 100.00
        x1 = [0]
        y1 = [0]
        x2 = [c]
        y2 = [d]  # we let a = 0, b = 0 so that the statrtingpoint is always the origin, makes computation quicker

        # finding the length of wire that we need to have a desired B-field at a certain point.
        desired_B = desiredB
        l = smp.Matrix([(a + t * ((c - a))), (b + (t) * (d - b)), 0])
        sep = r - l
        integrand = ((smp.diff(l, t)).cross(sep)) / (sep.norm() ** 3)
        print("This is the integrand for optimsation: ", integrand)
        mu = float(1.25663706 * 10 ** (-6))
        constant = float(mu * current * N / (4 * np.pi))
        # Subbing in initial value.

        integrandoptimise = integrand.subs(
            {a: x1[0], b: y1[0], x: pointofeval_x, y: pointofeval_y, z: pointofeval_z})

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

        # The user can change the accuracy of the optimiser by changing the number of data points
        # ThE user can also change the boundaries for c and d for the optimiser.
        d = np.linspace(0, 1, 100)
        c = np.linspace(0, 1, 100)
        stored_B_array = []
        # Tests all the values to find where the B-field is closest to the one we desire.
        for index in range(c.size):
            arr = []
            for count in range(d.size):
                val = np.linalg.norm(Boptimise(c[index], d[count]))
                arr.append(val)
            stored_B_array.append(arr)
        column_index = []
        min_values = []
        for index in range(c.size):
            row_array = np.array(stored_B_array[index])
            idx = np.abs(row_array - desired_B).argmin()
            min_values.append(row_array[idx])
            column_index.append(idx)
            row_array = np.append(row_array, stored_B_array[index][idx])

        idx = np.abs(np.abs(np.asarray(min_values) - desired_B)).argmin()
        d_val = column_index[idx]
        optimised_c = c[idx]
        optimised_d = d[d_val]
        # return print(" c= ", "{:e}".format(optimised_c), "d =", "{:e}".format(optimised_d))
        return c[idx], d[d_val]
        # print(c[idx])


    def BcircleOptimse(desiredB, center_x, center_y, pointofeval_x, pointofeval_y, pointofeval_z):
        """Function to optimise the B-field due to a circle centered at (ox,oy), the point of evaluation must be inputted.
        Can add an angle input for added functionality of allowing for arcs, but it is omitted to reduce the number of inputs
        required, as 2*pi would be needed to be inputted for a circle."""
        t, x, y, z = smp.symbols('t x y z')
        r = smp.Matrix([x, y, z])

        # User input of the desired B-field at the point, inputted as a float.
        desired_B = float(1)

        desired_B_array = [0, 0,
                           0]  # if you leave it as 0 then we just ignore the specific component, i.e. wont optimise for it.
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
        totalintegrandarc = smp.Matrix(
            [0, 0, 0])  # this leaves for multiple coil setup as you desire, ignored for now.

        # The total integrand arc is left here for future development where the user can input multiple coils (like a solenoid)
        # and optimise for a solenoid.
        l = smp.Matrix([smp.cos(t) + ox, smp.sin(t) + oy, height[0]])
        sep = r - l
        integrand = (smp.diff(l, t).cross(sep) / sep.norm() ** 3) * current
        totalintegrandarc = totalintegrandarc + integrand
        for con in range(3):
            totalintegrandarc[con] = constant * totalintegrandarc[con]
        dBxadt = smp.lambdify([t, x, y, z], totalintegrandarc[0])
        dByadt = smp.lambdify([t, x, y, z], totalintegrandarc[1])
        dBzadt = smp.lambdify([t, x, y, z], totalintegrandarc[2])