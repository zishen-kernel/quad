import threading
import socket
import codecs
import struct
import math
import quaternion
import live_line
import pygame
import td

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

    process()


def process():
    t = time.time()
    interval = 0.0

    if g['last_time'] != 0.0:
        interval = t - g['last_time']

        if interval > g['max_interval']:
            g['max_interval'] = interval

    g['last_time'] = t

    if interval > 0.05:
        print 'interval: %.2f %.2f' % (g['max_interval'], interval)

    print st
    test_acc()
    #test_magnet()
    #test_gyro()


def start_server(st):
    th = threading.Thread(target=runner, args=(st, ))
    th.daemon = True
    th.start()


t = {
        'sum_x': 0.0,
        'sum_y': 0.0,
        'sum_z': 0.0,
        'n': 0.0,
        }
def test_gyro():
    gyrox = st['gyrox']
    gyroy = st['gyroy']
    gyroz = st['gyroz']

    gyrox = gyrox / 32768.0 * 2000.0
    gyroy = gyroy / 32768.0 * 2000.0
    gyroz = gyroz / 32768.0 * 2000.0

    t['sum_x'] += gyrox
    t['sum_y'] += gyroy
    t['sum_z'] += gyroz
    t['n'] += 1.0

    n = t['n']
    print '%.4f %.4f %.4f' % (t['sum_x']/n, t['sum_y']/n, t['sum_z']/n)

    live_line_obj.data_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (244, 244, 244)
            ]

    data = [gyrox, gyroy, gyroz, gyroz]
    live_line_obj.feed(data)

def test_acc():
    accx = st['accx']
    accy = st['accy']
    accz = st['accz']


    accx = 4.0 * accx / 32768.0
    accy = 4.0 * accy / 32768.0
    accz = 4.0 * accz / 32768.0

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
    a1 = td_obj1.trace(mags[0])
    a2 = td_obj2.trace(mags[0])
    a3 = td_obj3.trace(mags[0])


    #control.run(accx, accy, accz)
    live_line_obj.data_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (244, 244, 244)
            ]

    #data = [mags[0], mags[1], mags[2], a]
    data = [mags[0], a3, a3, a3]
    live_line_obj.feed(data)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1800, 800))
    clock = pygame.time.Clock()

    live_line_obj = live_line.LiveLine(max_abs=2.0)
    td_obj1 = td.Tda(r=0.0001)
    td_obj2 = td.Tda(r=0.001)
    td_obj3 = td.Tdc()

    start_server(st)


    running = True

    while running:
        clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            live_line_obj.process_event(event)

        live_line_obj.draw(screen)

        pygame.display.flip()
