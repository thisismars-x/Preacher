'''
to 'move' the object we need two operations: 
translation:    handled within main function
rotation:       rotate()
'''

import math
from math import cos, sin, radians
import numpy as np

from declarations import *

def rotate(vertices, angle_x, angle_y):
    rotated_vertices = []

    '''
    standard rotation around y and x axes
    '''
    for x, y, z in vertices:

        temp_x = x * cos(radians(angle_y)) - z * sin(radians(angle_y))
        temp_z = x * sin(radians(angle_y)) + z * cos(radians(angle_y))
        x, z = temp_x, temp_z

        temp_y = y * cos(radians(angle_x)) - z * sin(radians(angle_x))
        temp_z = y * sin(radians(angle_x)) + z * cos(radians(angle_x))
        y, z = temp_y, temp_z

        rotated_vertices.append([x, y, z])

    return rotated_vertices

def projection(vertices, screen_width, screen_height, scale=ZOOM, translation=(0, 0)):

    projected_vertices = []
    '''
    go from 3d coords to 2d display
    uses perspective projection for projection
    scale:          controls size of projection [increase for more possible zooming]
    translation:    for shifting along (x, y)
    '''

    trans_x, trans_y = translation
    for x, y, z in vertices:
        f = scale / (z + 15)  
        x_proj = int(x * f + screen_width / 2 + trans_x)
        y_proj = int(-y * f + screen_height / 2 + trans_y)
        projected_vertices.append((x_proj, y_proj))

    return projected_vertices

