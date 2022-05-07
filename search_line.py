import numpy as np
import cv2
import pyvista as pv
import vtk
import shapely as sh
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


image_path = 'C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\pa0st0se2-targets\\'
cnt_array = []
approx_array = []
range_x1 = 20
range_x2 = 21
start_img = 88
scale = 491/192.1 # to px
slising_offset = 1.259*scale
image_ids = range(range_x1 + start_img, range_x2 + start_img)
for im in image_ids:
    image = cv2.imread(image_path + 'IM' + str(im) + '.png')
    
    # find line between green and white area in image
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    cv2.imshow('edges', edges)
    cv2.waitKey(0)
        