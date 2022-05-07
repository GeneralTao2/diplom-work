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

def func(str):
    time.sleep(2)
    print(str)

def kill_th(th):
    print("Thread had stopped!")
    if th.is_alive():
        th.stop()

th = StoppableThreadClass(target=func, args=("me!",))
th.start()
killer = threading.Thread(target=th, args=(th,))
killer.start()

