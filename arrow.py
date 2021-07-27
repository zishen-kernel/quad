from OpenGL.GL import *
import numpy
import uniform
import pyrr

def get_arrow_triangles(vector, height=0.2):
    normal = pyrr.vector3.normalize(vector)

    base_v = pyrr.Vector3(vector) - normal * height

    p_tmp = [0.0, 0.0, 0.0]
    min_index = vector.index(min(vector))
    p_tmp[min_index] = 1.0

    p_tmp = pyrr.Vector3(p_tmp)

    p1 = pyrr.vector3.cross(p_tmp, base_v)
    p2 = pyrr.vector3.cross(base_v, p1)

    p1 = pyrr.vector3.normalize(p1)
    p2 = pyrr.vector3.normalize(p2)

    p1_a = base_v + p1 * (height / 2.0)
    p1_b = base_v - p1 * (height / 2.0)

    p2_a = base_v + p2 * (height / 2.0)
    p2_b = base_v - p2 * (height / 2.0)

    triangles = [
            vector, p1_a.tolist(), p1_b.tolist(),
            vector, p2_a.tolist(), p2_b.tolist()
            ]

    return triangles

class Arrow:
    def __init__(self, color=None, origin=None, vector=None, length=1, tail=0):
        self.model = pyrr.matrix44.create_identity()
        if color is None:
            self.color = [1.0, 0.0, 0.0]
        else:
            self.color = color

        if origin is None:
            self.origin = [0.0, 0.0, 0.0]
        else:
            self.origin = origin

        if vector is None:
            self.vector = [1.0, 0.0, 0.0]
        else:
            self.vector = vector

        self.normalized = pyrr.vector3.normalize(self.vector)

        self.length = length
        self.tail = tail

        self.get_vertexs()

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

    def get_vertexs(self):
        end_p = (pyrr.Vector3(self.origin) +
                 self.normalized * self.length).tolist()

        start_p = (pyrr.Vector3(self.origin) -
                   self.normalized * self.tail).tolist()

        triangles = get_arrow_triangles(end_p)

        self.vertexs = []
        self.vertexs.extend(start_p)
        self.vertexs.extend(self.color)
        self.vertexs.extend(end_p)
        self.vertexs.extend(self.color)

        for p in triangles:
            self.vertexs.extend(p)
            self.vertexs.extend(self.color)


    def draw(self):
        uniform.set_use_color(1)
        uniform.set_model(self.model)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINES, 0, 2)
        glDrawArrays(GL_TRIANGLES, 2, 6)
