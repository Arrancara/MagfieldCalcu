import plotly.graph_objects as go
import numpy as np
from fields import Bfield


class Plotter:
    def __init__(self):
        pass

    def Bfieldplotter(self, filepath):
        # Change the array of x, to change where the scatter plot is plotted around
        start = -10
        stop = 10
        x = np.linspace(start, stop, 15)  # creates an array of points
        xv, yv, zv = np.meshgrid(x, x, x)
        x0 = xv.ravel()
        y0 = yv.ravel()
        z0 = zv.ravel()
        B = Bfield(filepath)
        dB = B.Bintegrand()
        dB_num = B.make_numeric(dB)
        tot = len(x0)
        B0 = np.zeros([tot, 3])

        for i, x in enumerate(x0):
            B0[i], _ = B.calculate_B_field(dB_num, (x0[i], y0[i], z0[i]))
            print(i + 1, 'of', tot)
        plot_type = 'iso'
        if plot_type == 'cone':
            data = go.Cone(x=x0, y=y0, z=z0, u=B0[:, 0], v=B0[:, 1], w=B0[:, 2],
                           colorscale='Inferno', colorbar=dict(title='$hello$'),
                           sizemode="scaled", visible=True)
        elif plot_type == 'stream':
            data = go.Streamtube(x=x0, y=y0, z=z0, u=B0[:, 0], v=B0[:, 1], w=B0[:, 2],
                                 colorscale='Inferno', colorbar=dict(title='$hello$'), visible=True,
                                 starts=dict(x=np.linspace(start, stop, 5), y=np.linspace(start, stop, 5),
                                             z=np.linspace(start, stop, 5)))
        elif plot_type == 'iso':
            Bnorm = np.sqrt(np.sum(B0**2, axis=1))
            data = go.Isosurface(x=x0, y=y0, z=z0, value=Bnorm,
                           colorscale='Inferno', colorbar=dict(title='$hello$'), visible=True,
                                 surface_count=20, opacity=0.25)

        layout = go.Layout(title=r'B-field',
                           scene=dict(xaxis_title=r'x',
                                      yaxis_title=r'y',
                                      zaxis_title=r'z',
                                      aspectratio=dict(x=1, y=1, z=1),
                                      camera_eye=dict(x=1.2, y=1.2, z=1.2)))
        factor = 1.2
        fig = go.Figure(data=data, layout_xaxis_range=[factor * start, factor * stop],
                        layout_yaxis_range=[factor * start, factor * stop])
        # Defines the range of the axis.
        fig.update_layout(
            scene=dict(
                xaxis=dict(nticks=4, range=[factor * start, factor * stop], ),
                yaxis=dict(nticks=4, range=[factor * start, factor * stop], ),
                zaxis=dict(nticks=4, range=[factor * start, factor * stop]), ),
            width=2500,
            margin=dict(r=100, l=10, b=10, t=10))
        fig.update_traces()
        fig.show()

        # fig, ax = plt.subplots(subpl  ot_kw={'aspect': 'equal'})
        # e = []
        # for s in shapes:
        #     if isinstance(s, Ellipse):
        #         print(s.x, s.y, s.rx, s.ry)
        #         e.append(Ell(xy=[s.x, s.y], width=2 * s.rx, height=2 * s.ry))
        #
        # print(e)
        # for ee in e:
        #     ax.add_artist(ee)
        #
        # ax.set_xlim([-300, 300])
        # ax.set_ylim([-300, 300])
        #
        # plt.show()


if __name__ == "__main__":
    pt = Plotter()
    filepath = r'C:\Users\Adam\Documents\Git\MagfieldCalcu'
    file = r'\test_ellipse.svg'
    pt.Bfieldplotter(filepath + file)
