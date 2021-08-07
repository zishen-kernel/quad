from OpenGL.GL import *
import numpy
import uniform
import pyrr

class Cube:
    def __init__(self, color=None):
        self.points = [
                [-1,-1,1], [1,-1,1], [1,1,1],
                [-1,-1,1], [1,1,1], [-1,1,1],
                [1,-1,1], [1,-1,-1], [1,1,-1],
                [1,-1,1], [1,1,-1], [1,1,1],
                [1,-1,-1], [-1,-1,-1], [-1,1,-1],
                [1,-1,-1], [-1,1,-1], [1,1,-1],
                [-1,-1,-1], [-1,-1,1], [-1,1,1],
                [-1,-1,-1], [-1,1,1], [-1,1,-1],
                [-1,1,1], [1,1,1], [1,1,-1],
                [-1,1,1], [1,1,-1], [-1,1,-1],
                [1,-1,1], [-1,-1,-1], [1,-1,-1],
                [1,-1,1], [-1,-1, 1], [-1,-1,-1],
                ]

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

    def draw(self, scale=None, position=None):
        if scale is None:
            scale = 1.0

        if position is None:
            position = [0.0, 0.0, 0.0]

        s = numpy.array([scale, scale, scale])
        m1 = pyrr.matrix44.create_from_scale(s)
        m2 = pyrr.matrix44.create_from_translation(position)
        m = pyrr.matrix44.multiply(m1, m2)
        uniform.set_model(m)

        uniform.set_use_color(1)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3 * 12)
