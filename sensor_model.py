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

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import time


st = {
        'v': [1.0, 1.0, 1.0],
        'angle': 0.0
        }

g = {
        'block': [' '] * 34,
        'block_len': 0,
        'marker_len': 0,
        'block_n': 0,

        'bytes_n': 0,
        'last_q': None,
        'c_out': False,
        'last_time': 0.0,
        'max_interval': 0.0,
        'mag_max': [0.14877, 0.155243, 0.18402],
        'mag_min': [-0.24292, -0.2294, -0.202179],
    }

def runner(st):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    sock.bind(("0.0.0.0", 3333))
    sock.listen(10)
    print 'tcp server start'

    fusion_obj = data_fusion.Fusion()
    g['fusion_obj'] = fusion_obj

    conn, addr = sock.accept()
    print conn
    print addr

    while True:
        data = conn.recv(40)
        if data == '':
            break

        #print len(data)
        #print time.time()
        g['bytes_n'] += len(data)
        process_data(st, data)

    print 'tcp server stop'

def process_data(st, data):

    for i in range(len(data)):
        feed(st, data[i])


def feed(st, b):
    if g['marker_len'] == 6:
        g['block'][g['block_len']] = b
        g['block_len'] += 1

        if g['block_len'] == 34:
            update(st)
            g['block_len'] = 0
            g['marker_len'] = 0

    else:
        if b == b'\xff':
            g['marker_len'] += 1
        else:
            g['marker_len'] = 0


def update(st):
    g['block_n'] += 1

    #hex_data = codecs.encode(g['block'], 'hex')
    #origin_data = hex_data.decode('hex')
    #print hex_data

    # qw, qi, qj, qk, accx, accy, accz
    # gyrox, gyroy, gyroz, magx, magy, magz

    data = ''.join(g['block']) 
    r = struct.unpack('ffffhhhhhhhhh', data)

    st['q'] = [r[0], r[1], r[2], r[3]]
    st['v'] = [r[1], r[2], r[3]]
    st['accx'] = r[4]
    st['accy'] = r[5]
    st['accz'] = r[6]

    st['gyrox'] = r[7]
    st['gyroy'] = r[8]
    st['gyroz'] = r[9]

    st['magx'] = r[10]
    st['magy'] = r[11]
    st['magz'] = r[12]

    data_set = {
            'gyro_q': [r[0], r[1], r[2], r[3]],
            'acc': [r[4], r[5], r[6]],
            'gyro': [r[7], r[8], r[9]],
            'mag': [r[10], r[11], r[12]]
            }
    g['fusion_obj'].feed(data_set)



def start_server(st):
    th = threading.Thread(target=runner, args=(st, ))
    th.daemon = True
    th.start()

def test_acc():
    accx = st['accx']
    accy = st['accy']
    accz = st['accz']


    accx = 2.0 * accx / 32768
    accy = 2.0 * accy / 32768
    accz = 2.0 * accz / 32768

    a = math.sqrt(accx * accx + accy * accy + accz * accz)

    #control.run(accx, accy, accz)
    live_line_obj.data_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (244, 244, 244)
            ]

    data = [accx, accy, accz, a]
    live_line_obj.feed(data)


def test_magnet():
    magx = st['magx']
    magy = st['magy']
    magz = st['magz']


    magx = magx / 32768.0
    magy = magy / 32768.0
    magz = magz / 32768.0

    mags = [magx, magy, magz]

    for i in range(3):
        if mags[i] > 0:
            mags[i] = mags[i] / g['mag_max'][i]
        else:
            mags[i] = -mags[i] / g['mag_min'][i]

    a = math.sqrt(mags[0] * mags[0] + mags[1] * mags[1] + mags[2] * mags[2])

    #control.run(accx, accy, accz)
    live_line_obj.data_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (244, 244, 244)
            ]

    data = [mags[0], mags[1], mags[2], a]
    live_line_obj.feed(data)

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

    start_server(st)

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
        #model3d_obj.draw(model_q=g['fusion_obj'].mag_fusion_obj.q)
        #model3d_obj.draw(model_q=g['fusion_obj'].adjusted_gyro_q)
        model3d_obj.draw(model_q=g['fusion_obj'].q)

        if g['fusion_obj'].adjusted_axis is not None:
            axis = g['fusion_obj'].adjusted_axis
            x_arrow = arrow.Arrow(color=[1.0, 0.0, 0.0],
                    vector=axis[0])
            #x_arrow.draw()

            y_arrow = arrow.Arrow(color=[0.0, 1.0, 0.0],
                    vector=axis[1])
            #y_arrow.draw()

            z_arrow = arrow.Arrow(color=[0.0, 0.0, 1.0],
                    vector=axis[2])
            #z_arrow.draw()

        if g['fusion_obj'].acc_normal is not None:
            cycle_obj = cycle.Cycle(cos=g['fusion_obj'].acc_normal[0])
            #cycle_obj.draw()

            cycle_obj = cycle.Cycle(cos=g['fusion_obj'].mag_normal[0],
                    nv=g['fusion_obj'].mag_v)
            #cycle_obj.draw()


        pygame.display.flip()

if __name__ == '__main__':
    run()
