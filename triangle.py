from OpenGL.GL import *
import numpy
import uniform
import pyrr

class Triangle:
    def __init__(self, points=None, color=None):

        if points is None:
            p1 = [-0.1, 2, 2]
            p2 = [0.5, 2, 1]
            p3 = [0.2,2, 4]
            p1 = (pyrr.Vector3(p1).normalized * 4.0).tolist()
            p2 = (pyrr.Vector3(p2).normalized * 4.0).tolist()
            p3 = (pyrr.Vector3(p3).normalized * 4.0).tolist()
            self.points = [
                p1,
                p2,
                p3,
                ]
        else:
            self.points = points

        if color is None:
            self.color = [1.0, 0.0, 0.0]
        else:
            self.color = color

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
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
