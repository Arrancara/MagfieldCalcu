import sympy as smp


class Ellipse:
    def __init__(self, x, y, rx, ry):
        self.rx = float(rx)
        self.ry = float(ry)
        self.x = float(x)
        self.y = float(y)

    def parametric(self, phi, height):
        # 0 <= phi <= 1
        t = smp.symbols(phi, real=True)
        x = self.rx * smp.cos(2 * smp.pi * t) + self.x
        y = self.ry * smp.sin(2 * smp.pi * t) + self.y
        ell = smp.Matrix([x, y, height])
        self.ell = ell


class Path:
    # only works for paths of straight segments
    def __init__(self, paths):
        self.paths = paths
        self.path_types = ['M', 'm', 'C', 'c', 'A', 'a', 'Z', 'z', 'l']

    def parse_path(self):
        x = self.paths.split()
        # path_types = [s for s in x if s in self.path_types]
        idx = [i for i, s in enumerate(x) if s in self.path_types]
        points = []

        if len(idx) == 1:
            points.append(x[idx[0] + 1:])
        else:
            for k in range(len(idx) - 1):
                points.append(x[idx[k] + 1: idx[k + 1]])

        points = points[0]
        points = [p.split(',') for p in points]
        pt = []
        for p in points:
            pt.append((float(p[0]), float(p[1])))

        segments = {'s' + str(n): {'start': [], 'end': []} for n in range(len(pt) - 1)}

        for k, p in enumerate(pt[:-1]):
            segments['s' + str(k)]['start'] = p
            segments['s' + str(k)]['end'] = pt[k + 1]

        self.segments = segments

    def parametric(self, t, height):
        # 0 <= t <= 1
        t = smp.symbols(t, real=True)
        ell = []
        for idx in self.segments:
            s = self.segments[idx]
            r0 = smp.Matrix([s['start'][0], s['start'][1], height])
            r1 = smp.Matrix([s['end'][0], s['end'][1], height])
            v = r1 - r0
            ell.append(r0 + t * v)

        self.ell = ell


class Rectangle:
    def __init__(self, x, y, width, height):
        self.height = float(height)
        self.width = float(width)
        self.x = float(x)
        self.y = float(y)
        self.calc_corners()

    def calc_corners(self):
        p1 = (self.x, self.y)
        p2 = (self.x + self.width, self.y)
        p3 = (self.x + self.width, self.y + self.height)
        p4 = (self.x, self.y + self.height)
        self.points = [p1, p2, p3, p4]

    def parametric(self, t, z):
        # 0 <= t <= 1
        t = smp.symbols(t, real=True)
        ell = []
        r_vec = []
        for p in self.points:
            r_vec.append(smp.Matrix([p[0], p[1], z]))

        for k, r in enumerate(r_vec[:-1]):
            v = r_vec[k + 1] - r
            ell.append(r + t * v)

        self.ell = ell
