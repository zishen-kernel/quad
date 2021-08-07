from OpenGL.GL import *
import numpy
import uniform
import pyrr
import cube

def draw_sensor_data(points):
    cube_obj = cube.Cube()

    for p in points:
        cube_obj.draw(scale= 0.007, position=p)
