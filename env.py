from OpenGL.GL import *
import numpy
import uniform
import pyrr

class Env:
    def __init__(self):
        self.vertexs = []
        self.color = [0.3, 0.4, 0.3]
        self.line_length = 10

        self.model = pyrr.matrix44.create_identity()

        for i in range(-10, 11, 2):
            self.vertexs.extend([i, 0, self.line_length])
            self.vertexs.extend(self.color)
            self.vertexs.extend([i, 0, -self.line_length])
            self.vertexs.extend(self.color)

            self.vertexs.extend([self.line_length, 0, i])
            self.vertexs.extend(self.color)
            self.vertexs.extend([-self.line_length, 0, i])
            self.vertexs.extend(self.color)


        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        self.vbo_data = numpy.array(self.vertexs, numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, self.vbo_data.nbytes,
                self.vbo_data, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0) #position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                6 * 4, ctypes.c_void_p(0))

        glEnableVertexAttribArray(2) #color
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                6 * 4, ctypes.c_void_p(12))

    def draw(self):
        uniform.set_use_color(1)
        uniform.set_model(self.model)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINES, 0,
                self.vbo_data.nbytes / 24)
