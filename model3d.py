import obj_loader
import uniform
import pyrr
from OpenGL.GL import *
import quaternion
import math

class Model3d:
    def __init__(self, obj_path, obj_file):
        self.groups = obj_loader.load(obj_path, obj_file)

        tran = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        rotation = pyrr.matrix44.create_from_y_rotation(-math.pi/2.0)
        self.tran_rot = pyrr.matrix44.multiply(tran, rotation)

        #rotation = pyrr.matrix44.create_from_x_rotation(-math.pi/2.0)
        rotation = pyrr.matrix44.create_from_x_rotation(0.0)
        self.tran_rot = pyrr.matrix44.multiply(self.tran_rot, rotation)

        self.rot_q = quaternion.from_axis_angle([-1.0, 0.0, 0.0], 90)

    def draw(self, model_q=None):
        if model_q is not None:
            axis, angle = quaternion.get_axis_angle(model_q)
            rot_axis = quaternion.rotate_vector(axis, self.rot_q)

            new_model_q = quaternion.from_axis_angle(rot_axis, angle)
            matrix_q = quaternion.q_to_matrix(new_model_q)
            self.model = pyrr.matrix44.multiply(self.tran_rot, matrix_q)
        else:
            self.model = self.tran_rot

        uniform.set_model(self.model)
        uniform.set_use_color(0)

        for i in range(len(self.groups)):
            group = self.groups[i]

            glBindVertexArray(group['vao'])

            #texture
            glBindTexture(GL_TEXTURE_2D, group['texture'])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER);
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER);

            image = group['image']
            image_data = group['image_data']
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                    0, GL_RGB, GL_UNSIGNED_BYTE, image_data)


            glDrawArrays(GL_TRIANGLES, 0, group['triangles'].nbytes/20)

