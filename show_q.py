import threading
import socket
import codecs
import struct
import math
import quaternion
import live_line
import pygame
import shader_loader
import camera
import uniform
import pyrr
import env
import coord
import model3d
import data_fusion
import cycle
import arrow
import util

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
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

def run():
    width = 1280
    height = 720

    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE)

    pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.OPENGL)

    program = get_program()
    model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    projection = pyrr.matrix44.create_perspective_projection_matrix(
            45, 1.0 * width / height, 0.1, 1000)
    uniform.get_locs(program)
    uniform.set_model(model)
    uniform.set_projection(projection)

    camera_obj = camera.Camera()
    env_obj = env.Env()
    coord_obj = coord.Coord()
    model3d_obj = model3d.Model3d('shangwu', 'part1.obj')

    infos = util.load_data('data.txt')
    print infos[0]
    print infos[1]
    qs = []
    for i in range(len(infos)):
        qs.append(infos[i]['data_fusion_q'])
    q_index = 0

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.TEXTINPUT:
                if event.text == 'n':
                    q_index += 1
                    print q_index
                    print qs[q_index]

            camera_obj.process_event(event)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        uniform.set_view(camera_obj.view)
        env_obj.draw()
        coord_obj.draw()
        model3d_obj.draw(model_q=qs[q_index])

        pygame.display.flip()

if __name__ == '__main__':
    run()
