
class plotter:
    def __init__(self):
        pass

    def Bfieldplotter(filepath):
        # Bintegrand function is ued to find the integrand of the path.
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

        # Change the array of x, to change where the scatter plot is plotted around
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
        # Defining the title, and the axis lables.
        layout = go.Layout(title=r'B-field',
                           scene=dict(xaxis_title=r'x',
                                      yaxis_title=r'y',
                                      zaxis_title=r'z',
                                      aspectratio=dict(x=1, y=1, z=1),
                                      camera_eye=dict(x=1.2, y=1.2, z=1.2)))
        fig = go.Figure(data=data, layout_yaxis_range=[-4, 4], layout_xaxis_range=[-4, 4])
        # Defines the range of the axis.
        fig.update_layout(
            scene=dict(
                xaxis=dict(nticks=4, range=[-5, 5], ),
                yaxis=dict(nticks=4, range=[-5, 5], ),
                zaxis=dict(nticks=4, range=[-5, 5]), ),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10))
        fig.show()
        HTML(fig.to_html())