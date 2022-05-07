import numpy as np
import cv2
import pyvista as pv
import vtk
import shapely as sh
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


pa0st0se2=pv.read("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\models\\pa0st0se2_o3d_lite.ply")
p = pv.Plotter()
#p.add_mesh(pa0st0se2, show_edges=True, color="white")
p.add_points(pa0st0se2.points, scalar_bar_args={'title': 'Z Position'})
#p.show()
pa0st0se2.plot(show_edges=True, color="white")