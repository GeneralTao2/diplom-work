import numpy as np
import cv2
import pyvista as pv
import vtk
import shapely as sh
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

vrtx_qty = 343

scale = 491/192.1 # to px

image_path = 'C:/Users/gener/OneDrive/Documents/Python/images-to-stl/images/pa0st0se2-targets/'
cnt_array = []
approx_array = []
range_x1 = 0
range_x2 = 37
start_img = 88
slising_offset = 1.259*scale
image_ids = range(range_x1 + start_img, range_x2 + start_img)

def plotPolygon(polygon, style):
    x = []
    y = []
    for v in polygon:
        x.append(v[0])
        y.append(v[1])
    plt.plot(x, y, style)

for im in image_ids:
    image = cv2.imread(image_path + 'IM' + str(im) + '.png')
    """ cv2.imshow('shapes', image)
    cv2.waitKey(0)  """
    b,g,r = cv2.split(image)
    #cv2.imshow("winname1", image)

    lower_green = np.array([0,100,0])
    upper_green = np.array([50,255,50])

    mask = cv2.inRange(image,lower_green,upper_green)
    mask_rgb = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    image = image & mask_rgb
    
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("winname", imgGray)
    #cv2.waitKey(0)
    _, thresh = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = contours[0]
    approx = cv2.approxPolyDP(cnt, 0.000001*cv2.arcLength(cnt, True), True)
    cnt_array.append(cnt)
    #print(approx)
    approx_array.append(approx)

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def toStructoredArray(polygon):
    retval = []
    for v in polygon:
        retval.append([v[0][0], v[0][1]])
    return retval



def smoothPolygon(poly):
    length = len(poly)
    smoothed_raw = []
    for i in range(length-1):
        dx = poly[i][0] - poly[i+1][0]
        dy = poly[i][1] - poly[i+1][1]
        newx = poly[i][0] - dx/2
        newy = poly[i][1] - dy/2
        smoothed_raw.append([newx, newy])
    dx = poly[length-1][0] - poly[0][0]
    dy = poly[length-1][1] - poly[0][1]
    newx = poly[length-1][0] - dx/2
    newy = poly[length-1][1] - dy/2
    smoothed_raw.append([newx, newy])
    return smoothed_raw

def averageEdgeLength(poly):
    length = len(poly)
    total = 0
    for i in range(length-1):
        dx = poly[i][0] - poly[i+1][0]
        dy = poly[i][1] - poly[i+1][1]
        total += np.sqrt(dx*dx + dy*dy)
    dx = poly[length-1][0] - poly[0][0]
    dy = poly[length-1][1] - poly[0][1]
    total += np.sqrt(dx*dx + dy*dy)
    return total / length

def minimalEdgeLength(poly):
    length = len(poly)
    min_length = float('inf')
    for i in range(length-1):
        dx = poly[i][0] - poly[i+1][0]
        dy = poly[i][1] - poly[i+1][1]
        length = np.sqrt(dx*dx + dy*dy)
        if length < min_length:
            min_length = length
    """ dx = poly[length-1][0] - poly[0][0]
    dy = poly[length-1][1] - poly[0][1]
    length = np.sqrt(dx*dx + dy*dy)
    if length < min_length:
        min_length = length """
    return min_length

def maximumEdgeLength(poly):
    length = len(poly)
    max_length = 0
    ret_index = 0
    for i in range(length-1):
        dx = poly[i][0] - poly[i+1][0]
        dy = poly[i][1] - poly[i+1][1]
        length = np.sqrt(dx*dx + dy*dy)
        if length > max_length:
            max_length = length
            ret_index = i
    return (max_length, ret_index)



# add vertices to polygon while maximum edge length is less than average edge length
def addVerticesUntilAvg(poly):
    length = len(poly)
    avg = averageEdgeLength(poly)
    max_length, ret_index = maximumEdgeLength(poly)
    while max_length > avg:
        dx = poly[ret_index][0] - poly[ret_index+1][0]
        dy = poly[ret_index][1] - poly[ret_index+1][1]
        newx = poly[ret_index][0] - dx/2
        newy = poly[ret_index][1] - dy/2
        poly.insert(ret_index+1, [newx, newy])
        max_length, ret_index = maximumEdgeLength(poly)
    return poly

def addVerticesUntilNumber(poly, number):
    length = len(poly)
    while length < number:
        _, ret_index = maximumEdgeLength(poly)
        dx = poly[ret_index][0] - poly[ret_index+1][0]
        dy = poly[ret_index][1] - poly[ret_index+1][1]
        newx = poly[ret_index][0] - dx/2
        newy = poly[ret_index][1] - dy/2
        poly.insert(ret_index+1, [newx, newy])
        length += 1
    return poly

def listToArray(poly):
    length = len(poly)
    retval = []
    for i in range(length):
        retval.append([poly[i][0], poly[i][1]])
    return retval

def gaussFunction(x):
    sigma = np.sqrt(2)
    mu = 1
    return 1/(sigma*np.sqrt(2*np.pi))*np.exp(-(x-mu)**2/(2*sigma**2))

#for a in range(len(approx_array)):
bufferd_poly_array = []
raw_mlop = 0 # maximum length of polygon
mlop = 0
idx_of_mlop = 0
image_qnt = len(image_ids)
for a in range(image_qnt):
    raw = cnt_array[a]
    #exit()

    length = len(raw)
    structured_raw = toStructoredArray(raw)
    structured_approx = toStructoredArray(approx_array[a])

    smoothed_raw = []
    dx=0
    dy=0
    newx=0
    new=0


    smoothed_raw = smoothPolygon(structured_raw)
    smoothed_approx = smoothPolygon(structured_approx)
    structured_approx.append(structured_approx[0])
    polygon_obj = Polygon(smoothed_approx).buffer(30, resolution=13, join_style=1).buffer(-30, resolution=13, join_style=1)
    buffered_approx_list = list(polygon_obj.exterior.coords)
    buffered_approx_array = listToArray(buffered_approx_list)
    buffered_array_length = len(buffered_approx_array)
    
    if(buffered_array_length > raw_mlop):
        raw_mlop = buffered_array_length
        idx_of_mlop = a
    bufferd_poly_array.append(buffered_approx_array)

#filled_approx_array = addVerticesUntilAvg(bufferd_poly_array[idx_of_mlop])  
#mlop = len(filled_approx_array)
##print(mlop)
##print(idx_of_mlop)
#
#
#filled_poly_array = []
#for a in range(image_qnt):
#    if(a == idx_of_mlop):
#        filled_poly_array.append(filled_approx_array)
#    else:
#        filled_poly_array.append(addVerticesUntilNumber(bufferd_poly_array[a], mlop))    

raw_points = []

for i in range(len(bufferd_poly_array)):
    for j in range(len(bufferd_poly_array[i])):
        #print(approx_array[i][j])
        raw_points.append([bufferd_poly_array[i][j][0], bufferd_poly_array[i][j][1], i*slising_offset])
points = pv.wrap(np.array(raw_points))
#surf = points.reconstruct_surface(nbr_sz=20, sample_spacing=4)
##surf
#
#pl = pv.Plotter(shape=(1,2))
#pl.add_mesh(points)
#pl.add_title('Point Cloud of 3D Surface')
#pl.subplot(0,1)
#pl.add_mesh(surf, color=True, show_edges=True)
#pl.add_title('Reconstructed Surface')
#pl.show()

import open3d as o3d
print("Testing mesh in Open3D...")
mesh = o3d.io.read_triangle_mesh("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\models\\pa0st0se2_raw.ply")
mesh.compute_vertex_normals()
mesh.paint_uniform_color([1, 0.706, 0])
pcd = o3d.geometry.PointCloud()
pcd = mesh.sample_points_poisson_disk(int(len(mesh.vertices)/40))
#pcd.points = o3d.utility.Vector3dVector(np.array(raw_points))
#o3d.visualization.draw_geometries([pcd])
alpha = 10
print(f"alpha={alpha:.3f}")


#mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=12)
#mesh = mesh.filter_smooth_laplacian(1)
##mesh = mesh.filter_smooth_simple(1)
#mesh = mesh.filter_smooth_taubin(3)
radii = [0.005, 0.01, 0.02, 0.04]
#rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
#    pcd, o3d.utility.DoubleVector(radii))

mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

o3d.io.write_triangle_mesh("C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\models\\pa0st0se2_o3d_lite.ply", mesh)

exit()
tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)
for alpha in np.logspace(np.log10(0.5), np.log10(0.01), num=4):
    print(f"alpha={alpha:.3f}")
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
        pcd, alpha, tetra_mesh, pt_map)
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)