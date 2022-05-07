import numpy as np
import cv2
import pyvista as pv
import vtk
import shapely as sh
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import create_sphere_sector as cs
import threading
from StoppableThread import *
import time
from matplotlib.colors import ListedColormap

import json
from VolumeIndexClass import *

data = None

with open("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\jsons\\vi_corrected.json") as json_file:
    data = json.load(json_file)

volume_index_array = [VolumeIndex(**(dict)) for dict in data]

volume_index_array.sort(key=lambda x: x.volume, reverse=True)
#[print(vi.idx, vi.volume) for vi in volume_index_array]

#=========================

pa0st0se2=pv.read("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\models\\pa0st0se2_o3d.ply")
center_pos = (256, 256, 0)
box_size = (5, 5, 5)
sphere = pv.Sphere(radius=10, center=center_pos, theta_resolution=50, phi_resolution=50)

sector = cs.SphereSector(0.80, 90, 10) #todo


pa0st0se2 = pa0st0se2.compute_normals()
pa0st0se2_tr = pa0st0se2.triangulate()



#pa0st0se2.plot_normals(mag=10, color='yellow', show_edges=True)

#arrow = pv.Arrow(start=(0, 0, 0), direction=(0, 0, 10), tip_length=50, tip_radius=2, shaft_radius=1, shaft_resolution=5)
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b



colors = np.full((len(pa0st0se2.points), 4), [227/256, 227/256, 227/256, 1])
max_volume = volume_index_array[0].volume
min_volume = volume_index_array[-2].volume #todo remove zeros
for vi in volume_index_array:
    if(vi.volume < 10):
        continue
    #mapped = 256 - translate(vi.volume, min_volume, max_volume, 0, 227)
    r, g, b = rgb(min_volume, max_volume, vi.volume)
    #colors[vi.idx] = [256/256.0, gb/256.0, gb/256.0, 1]
    colors[vi.idx] = [r/256.0, g/256.0, b/256.0, 1]
    #colors[vi.idx] = [0, 1.0, 0, 1]
    
my_colormap = ListedColormap(colors)
pa0st0se2.point_data['colors'] = colors

pl = pv.Plotter()
pl.add_mesh(pa0st0se2, opacity=1, scalars='colors',
                     rgb=True, preference='point')
#pl.add_mesh(sector.sector, opacity=1)
pl.show()

#for vi in [volume_index_array[1173]]:
#for vi in volume_index_array:
#    i = vi.idx
#    sector.move_to_and_rotate_foward(pa0st0se2.points[i], pa0st0se2.active_normals[i])
#    #if(vi.volume > 10):
#    #    continue
#    #if(vi.idx != 1173):
#    #    continue
#    print(i)
#    pl = pv.Plotter()
#    pl.add_mesh(pa0st0se2, opacity=0.8, scalars='colors',
#                     rgb=True, preference='point')
#    pl.add_mesh(sphere, color='red')
#    pl.add_mesh(sector.sector, opacity=0.5)
#    pl.show_grid()
#    result = sector.sector.boolean_intersection(pa0st0se2_tr, tolerance=1e-01, progress_bar=True)
#    #print(result.n_points)
#    #print(result.n_cells)
#    if(result.n_points != 0):
#        print(result.volume)
#        pl.add_mesh(result)
#    pl.show()
#
## 887
