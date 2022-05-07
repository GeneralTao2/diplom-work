import pyvista as pv
import matplotlib.pyplot as plt
import numpy as np
import math

def angle_betwee_vectors(vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    return np.arccos(np.clip(dot_product, -1.0, 1.0))

class SphereSector:
    def __init__(self, angel, sector_length, sector_offset):
        self.sector = self.create_sphere_sector(angel)
        #self.sector.rotate_vector((1, 0, 0), 180)
        #self.sector.translate((0, 0, 1))
        self.sector.translate(np.subtract((0, 0, 0),  self.sector.center))
        self.scale(sector_length)
        self.sector_length = sector_length
        self.sector_offset = sector_offset
        self.current_direction = (0, 0, 1)
        self.last_offset = (0, 0, 0)

    def create_sphere_sector(self, angel):
        pos=(0,0,0)
        radius= 1
        direction = (0,0,1)
        dx = 1
        cone_radius = (radius+dx)*np.tan(angel)
        sphere = pv.Sphere(radius=radius, center=pos, theta_resolution=50, phi_resolution=50)
        cone = pv.Cone(center=(0 + pos[0], 0. + pos[1], -(dx+radius)/2. + pos[2]), direction=direction, radius=cone_radius, height=radius+dx, resolution=80).triangulate()
        return cone.boolean_intersection(sphere)
    
    def scale(self, scale_factor):
        self.sector.scale((scale_factor, scale_factor, scale_factor))
    
    def move_to(self, pos):
        center = self.sector.center
        self.sector.translate(np.subtract(pos, center))

    
    def rotate_toward(self, direction, normalize=False):
        if normalize:
            direction = direction / np.linalg.norm(direction)
        axe = np.cross(direction, self.current_direction)
        angel = math.degrees(angle_betwee_vectors(direction, self.current_direction))
        self.sector.rotate_vector(axe, -angel)
        current_direction = direction

    def move_to_and_rotate_foward(self, pos, direction, normalize=False):
        if normalize:
            direction = direction / np.linalg.norm(direction)
        axe = np.cross(direction, self.current_direction)
        if(not any(axe)):
            axe = (1,0,0)
        angel = math.degrees(angle_betwee_vectors(direction, self.current_direction))
        self.sector.translate(np.subtract(self.last_offset, self.sector.center))
        #self.sector.rotate_vector(axe, -angel)
        #print(self.sector.center)
        self.sector.rotate_vector(axe, -angel)
        #print(self.sector.center)
        self.last_offset = self.sector.center
        #self.sector.translate(np.subtract((0, 0, 0), self.sector.center))
        self.sector.translate(np.dot(direction, -self.sector_length/2. + self.sector_offset))
        self.sector.translate(pos)
        self.current_direction = direction


#angel = 0.34
#sphereSector = SphereSector(angel, 10, 1)
#sphereSector1 = SphereSector(angel, 3, 1)
#direction = (0, 0, 1)
#ndirection = direction / np.linalg.norm(direction)
#
#arrow1_start=(0, 0, 0)
#arrow1_direction=(0.5, 0.5, 0)
#arrow1_ndirection = arrow1_direction / np.linalg.norm(arrow1_direction)
#arrow1 = pv.Arrow(start=arrow1_start, direction=arrow1_ndirection)
#
#arrow2_start=(3, 0, 0)
#arrow2_direction=(0.5, 0.5, -1)
#arrow2_ndirection = arrow2_direction / np.linalg.norm(arrow2_direction)
#arrow2 = pv.Arrow(start=arrow2_start, direction=arrow2_ndirection)
#
#arrow3_start=(0, 0, 0)
#arrow3_direction=(0,0,1)
#arrow3_ndirection = arrow3_direction / np.linalg.norm(arrow3_direction)
#arrow3 = pv.Arrow(start=arrow3_start, direction=arrow3_ndirection)
#
#
#
#sphereSector.move_to_and_rotate_foward(arrow1_start, arrow1_ndirection)
#sphereSector.move_to_and_rotate_foward(arrow2_start, arrow2_ndirection)
#sphereSector.move_to_and_rotate_foward(arrow3_start, arrow3_ndirection)
##sphereSector.move_to_and_rotate_foward(arrow1_start, arrow1_direction)
##sphereSector.move_to_and_rotate_foward2(arrow1_start, arrow1_direction)
##sphereSector1.move_to_and_rotate_foward2(arrow1_start, arrow1_direction)
##sphereSector.move_to_and_rotate_foward(arrow2_start, arrow2_ndirection)
##sphereSector.move_to_and_rotate_foward(arrow2_start, arrow2_ndirection)
##sphereSector.move_to_and_rotate_foward1(arrow3_start, arrow3_ndirection)
##sphereSector.move_to_and_rotate_foward1(arrow2_start, arrow2_ndirection)
##sphereSector.move_to_and_rotate_foward2(arrow1_start, arrow1_ndirection)
#
#
##sphereSector.move_to(arrow1_start)
##sphereSector.rotate_toward(arrow1_ndirection)
##sphereSector.move_to(arrow1_start)
#
##sphereSector.rotate_toward(arrow2_ndirection)
##sphereSector.move_to(arrow2_start)
#
#pl = pv.Plotter()
#pl.add_mesh(sphereSector.sector, show_edges=True, color="white")
#pl.add_mesh(sphereSector1.sector, opacity=0.5, color="blue")
#pl.add_mesh(arrow1, color="yellow")
#pl.add_mesh(arrow2, color="yellow")
#pl.add_mesh(arrow3, color="yellow")
#pl.show()