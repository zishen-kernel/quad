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
import quad.util
import quad.get_info
import cube
import mag_sensor
import pickle

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
    cube_obj = cube.Cube()
    model3d_obj = model3d.Model3d('shangwu', 'part1.obj')

    fd = open('sensor_data.txt', 'rb')
    #fd = open('calli_data.txt', 'rb')
    mag = pickle.load(fd)
    print mag[:10]

    running = True
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            camera_obj.process_event(event)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        uniform.set_view(camera_obj.view)
        env_obj.draw()
        coord_obj.draw()
        #model3d_obj.draw(model_q=g['q'])
        mag_sensor.draw_sensor_data(mag)
        #cube_obj.draw(scale=0.1, position=[0.0, 2.0, 0.0])

        pygame.display.flip()

if __name__ == '__main__':
    run()
