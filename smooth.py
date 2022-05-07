import numpy as np
import cv2
import pyvista as pv
import vtk
import shapely as sh
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

""" import trimesh
pa0st0se1_trimesh=trimesh.exchange.load.load("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\pa0st0se1.ply", "ply")
pa0st0se2_trimesh=trimesh.exchange.load.load("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\pa0st0se2.ply", "ply")
trimesh.export("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\pa0st0se1_trimesh.stl", "stl")
trimesh.export("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\pa0st0se2_trimesh.stl", "stl") """

sc = 1/(491/192.1)
pa0st0se2=pv.read("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\models\\pa0st0se2.ply")
pa0st0se1=pv.read("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\models\\pa0st0se1.ply")
""" pa0st0se1.scale([sc, sc, sc])
pa0st0se2.scale([sc, sc, sc]) """
""" pa0st0se1.save("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\pa0st0se1.stl")
pa0st0se2.save("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\pa0st0se2.stl") """

#pv.pa0st0se1.plot(show_edges=True)
#pv.pa0st0se2.plot(show_edges=True)
#cpos = mesh.plot()

""" pa0st0se2.scale([10.0, 10.0, 10.0])
print(resized) """
#surf.plot(show_edges=True)

pl = pv.Plotter(shape=(1,2))
pl.subplot(0,0)
pl.show_axes()
pl.show_grid()
pl.add_mesh(pa0st0se1)
pl.subplot(0,1)
pl.show_axes()
pl.show_grid()
pl.add_mesh(pa0st0se2)
pl.show()