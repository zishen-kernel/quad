import pygame
import obj_loader
import shader_loader
import uniform
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import triangle
import numpy

import time

def get_program():
    glEnable(GL_DEPTH_TEST)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    v_shader = shader_loader.load(GL_VERTEX_SHADER, 'shaders/v_shader_src')
    f_shader = shader_loader.load(GL_FRAGMENT_SHADER, 'shaders/f_shader_src')

    program = compileProgram(v_shader, f_shader)

    glUseProgram(program)

    return program

def draw(program, groups):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    rot = pyrr.Matrix44.from_x_rotation(time.time() / 10.0)
    model = pyrr.matrix44.multiply(model, rot)

    rot = pyrr.Matrix44.from_y_rotation(time.time() / 10.0)
    model = pyrr.matrix44.multiply(model, rot)

    view = pyrr.matrix44.create_look_at(pyrr.Vector3([-34, 0, 0]),
            pyrr.Vector3([0, 0, 0]),
            pyrr.Vector3([0, 1, 0]))

    projection = pyrr.matrix44.create_perspective_projection_matrix(
            45, 1280.0 / 720, 0.1, 100000)


    uniform.get_locs(program)

    uniform.set_model(model)
    uniform.set_view(view)
    uniform.set_projection(projection)
    uniform.set_use_color(0)

    for i in range(len(groups)):

        group = groups[i]

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



def run():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE)

    pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.OPENGL)


    program = get_program()

    groups = obj_loader.load('jet', 'jet.obj')


    running = True

    clock = pygame.time.Clock()

    while running:
        clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        draw(program, groups)

        pygame.display.flip()

if __name__ == '__main__':
    run()
