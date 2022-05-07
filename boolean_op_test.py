import pyvista as pv
import numpy as np
pos=(0,0,0)
radius=10
direction = (0,0,1)
dx = 20
angel = 0.52
cone_radius = (radius+dx)*np.tan(angel)

sphere_a = cone = pv.Cone(center=(0 + pos[0], 0. + pos[1], -(dx+radius)/2. + pos[2]), direction=direction, radius=cone_radius, height=radius+dx, resolution=100).triangulate()
sphere_b = pv.Sphere(radius=radius, center=pos, theta_resolution=50, phi_resolution=50)

result = sphere_a.boolean_intersection(sphere_b)
pl = pv.Plotter()
_ = pl.add_mesh(sphere_a, color='r', style='wireframe', line_width=3)
_ = pl.add_mesh(sphere_b, color='b', style='wireframe', line_width=3)
_ = pl.add_mesh(result, color='tan')
pl.camera_position = 'xz'
pl.show()