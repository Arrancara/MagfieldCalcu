
class Bfield:
    def __init__(self):
        pass

    def Bintegrand(filepath):
        parsingfunction(filepath)
        global totalintegrandarc
        totalintegrandarc = smp.Matrix([0, 0, 0])
        global totalintegrandline
        totalintegrandline = smp.Matrix([0, 0, 0])
        u = 0
        d_x = []
        d_y = []
        for index in range(len(line_loc)):  # we want to sort out the straight lines now.
            d_x.append(int(x2[u] - x1[u]))
            d_y.append(int(y2[u] - y1[u]))
            l = smp.Matrix([(x1[u] + t * (d_x[u])), (y1[u] + (t) * (d_y[u])), 0])
            sep = r - l
            integrand = currentline[u] * ((smp.diff(l, t).cross(sep)) / sep.norm() ** 3)
            u = u + 1
            totalintegrandline = integrand + totalintegrandline

            # lx.append(l[0])
            # ly.append(l[1])
            # ly.append(l[2])
        for i in range(len(radius)):
            l = smp.Matrix([smp.cos(k[i] * t) + ox[i], smp.sin(k[i] * t) + oy[i], height[i]])
            sep = r - l
            integrand = (smp.diff(l, t).cross(sep) / sep.norm() ** 3) * currentcircle[i]
            totalintegrandarc = totalintegrandarc + integrand
            i = i + 1

        print(totalintegrandline, "totalintegrandline")
        print(totalintegrandarc, "totalintegrandarc")
        return totalintegrandarc, totalintegrandline

    def Bfinder(filepath, x_cord, y_cord, z_cord):
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

        # Function defined that is used to calculate the B-field at a certain point.
        def B(x, y, z):
            return np.array(([(quad(dBxldt, 0, 1, args=(x, y, z))[0] + quad(dBxadt, 0, 2 * np.pi, args=(x, y, z))[0]),
                              (quad(dByldt, 0, 1, args=(x, y, z))[0] + quad(dByadt, 0, 2 * np.pi, args=(x, y, z))[0]),
                              (quad(dBzldt, 0, 1, args=(x, y, z))[0] + quad(dBzadt, 0, 2 * np.pi, args=(x, y, z))[0])]))

        print(B(x_cord, y_cord, z_cord))