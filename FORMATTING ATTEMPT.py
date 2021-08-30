import numpy as np

from scipy.integrate import quad
from sympy.interactive import printing

printing.init_printing(use_latex=True)  # Prints results in latex format

t, x, y, z = smp.symbols('t x y z')
r = smp.Matrix([x, y, z])  # position vector of an arbitrary point
mu = 1.25663706e-6







Blineoptimise(1, 1, 1, 1)


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


BcircleOptimse(1, 0, 0, 1, 1, 1)

# This requires the user to input a function in cartesian coordinates in vector form,
# this will be used to define "l", there is a limit to how the functions an be inputted, it must be parameterised
# using the letter "t" as the integrating function.


# def Bfieldfunction(function_x,function_y,function_z):
#     t, x, y, z = smp.symbols('t x y z')
#     r = smp.Matrix([x, y, z])
#     l = smp.Matrix([function_x,function_y,function_z])
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
#     aux = np.linspace(0,2*np.pi,100)
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
