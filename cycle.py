from OpenGL.GL import *
import numpy
import uniform
import pyrr
import quaternion
import math

class Cycle:
    def __init__(self, r=1.0, cos=0.7, nv=None, color=None, fine_n=200):
        self.r = r
        self.cos = cos
        self.fine_n = fine_n
        self.points = []
        self.model = pyrr.matrix44.create_identity()

        if nv is None:
            self.nv = [0.0, 1.0, 0.0]
        else:
            self.nv = quaternion.normal(nv) 

        if self.nv == [0.0, 1.0, 0.0]:
            self.rot_q = [1.0, 0.0, 0.0, 0.0]
        else:
            self.rot_q = quaternion.from_two_vector([0.0, 1.0, 0.0], self.nv)

        if color is None:
            self.color = [1.0, 0.0, 0.0]
        else:
            self.color = color

        sin = math.sqrt(1.0 - cos * cos)

        point = [sin, cos, 0.0]

        q_step = quaternion.from_axis_angle([0.0, 1.0, 0.0], 360.0 / self.fine_n)

        for i in range(self.fine_n):
            self.points.append(point)
            point = quaternion.rotate_vector(point, q_step)

        for i in range(len(self.points)):
            self.points[i] = quaternion.rotate_vector(self.points[i], self.rot_q)

        self.vertexs = []

        for point in self.points:
            self.vertexs.extend(point)
            self.vertexs.extend(self.color)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        self.vbo_data = numpy.array(self.vertexs, numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, self.vbo_data.nbytes,
                self.vbo_data, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0) #position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))

        glEnableVertexAttribArray(2) #color
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(12))

    def draw(self):
        uniform.set_use_color(1)
        uniform.set_model(self.model)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINES, 0, self.fine_n)
