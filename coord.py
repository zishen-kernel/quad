from OpenGL.GL import * 
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy
import obj_loader
import pyrr
from PIL import Image
import uniform
import socket
import codecs
import struct
import math
import arrow
import triangle


class Coord:
    def __init__(self):
        self.x_arrow = arrow.Arrow(color=[1.0, 0.0, 0.0],
                vector=[1.0, 0.0, 0.0], length=2.0, tail=2.0)

        self.y_arrow = arrow.Arrow(color=[1.0, 1.0, 0.0],
                vector=[0.0, 1.0, 0.0], length=2.0, tail=2.0)

        self.z_arrow = arrow.Arrow(color=[1.0, 1.0, 1.0],
                vector=[0.0, 0.0, 1.0], length=2.0, tail=2.0)

    def draw(self):
        self.x_arrow.draw()
        self.y_arrow.draw()
        self.z_arrow.draw()
