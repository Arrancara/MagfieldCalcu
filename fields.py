from parse import FileParser
import numpy as np
import sympy as smp
import scipy.integrate as int
import shapes


class Bfield:
    def __init__(self, filepath):
        par = FileParser()
        self.shapes = par.svgparser(filepath)
        mu0 = 4 * np.pi * 1e-7
        prefactor = mu0 / (4 * np.pi)

    def biot_savart(self, ell, t, field_point, current):
        sep = field_point - ell
        dB = current * (smp.diff(ell, t).cross(sep)) / sep.norm() ** 3
        return dB

    def Bintegrand(self):
        dB = []
        x, y, z, t, phi = smp.symbols('x y z t phi', real=True)
        field_point = smp.Matrix([x, y, z])
        for shape in self.shapes:
            if isinstance(shape, (shapes.Path, shapes.Rectangle)):
                for segment in shape.ell:
                    dB.append(self.biot_savart(segment, t, field_point, 1))
            if isinstance(shape, shapes.Ellipse):
                dB.append(self.biot_savart(shape.ell, t, field_point, 1))

        return dB

    def make_numeric(self, dB_list):
        dB_num = ([], [], [])
        x, y, z, t, phi = smp.symbols('x y z t phi', real=True)
        for dB in dB_list:
            for k in range(3):
                dB_num[k].append(smp.lambdify([t, x, y, z], dB[k]))

        return dB_num

    def calculate_B_field(self, dB_num, field_point):
        B = [0, 0, 0]
        Q = []
        error = np.zeros([len(dB_num[0]), 3])
        x, y, z = field_point
        for k in range(3):
            for s, dB in enumerate(dB_num[k]):
                Q.append(int.quad(dB, 0, 1, args=(x, y, z)))
                B[k] += Q[-1][0]
                error[s][k] = Q[-1][1]

        return B, error


if __name__ == "__main__":
    filepath = r'C:\Users\Adam\Documents\Git\MagfieldCalcu\test_ellipse.svg'
    B = Bfield(filepath)
    dB = B.Bintegrand()
    dB_num = B.make_numeric(dB)
    field_point = (1, 2, 3)
    B, errors = B.calculate_B_field(dB_num, field_point)
    print('B', field_point, ' = ', B)
