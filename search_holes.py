import numpy as np
import cv2
import pyvista as pv
import vtk
import shapely as sh
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

pa0st0se2=pv.read("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\models\\pa0st0se2.vtk")
idx = 9140
pa0st0se2 = pa0st0se2.compute_normals()
normal = pa0st0se2.active_normals[idx]
pos = start=pa0st0se2.points[idx]


pa0st0se2 = pa0st0se2.triangulate()
cyl = pv.Cone(center=(0. + pos[0], 0. + pos[1], 0. + pos[2]), direction=normal, radius=20, height=40, resolution=100).triangulate()
sphere = pv.Sphere(radius=20, center=(0,0,0), theta_resolution=50, phi_resolution=50)

pl = pv.Plotter()
pl.add_mesh(cyl, color="blue")
pl.add_mesh(pa0st0se2, opacity=0.4)
#pl.add_mesh(sphere, color="green")

#cyl.translate((0., value, 0))
#result = pa0st0se2.boolean_intersection(cyl)
#pl.add_mesh(result)

pl.show()


#pl.add_mesh(result, show_edges=True)
#def smooothRoutine(value):
#    global cyl
#    global pa0st0se2
#    global actor
#    global pl
#    cyl.translate((0., value, 0))
#    result = pa0st0se2.boolean_intersection(cyl)
#    if actor:
#        pl.remove_actor(actor)
#    actor = pl.add_mesh(result)

#pl.add_slider_widget(
#    callback=lambda value: smooothRoutine(int(value)),
#    rng=[-20, 20],
#    value=0,
#    title="test",
#    pointa=(.025, .1), pointb=(.31, .1),
#    style='modern',
#) 



#pl.add_mesh(pa0st0se2)
#pl.add_mesh(cyl)
#pl.add_mesh(result)