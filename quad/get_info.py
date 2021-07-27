import socket
import time
import struct
import util


def show_angle(info):
    ang = util.get_diff_angle(info)
    axis_ang = util.get_axis_diff_angle(info)
    print 'angle: %.2f  x: %.2f  y: %.2f  z: %.2f' % (
            ang, axis_ang[0], axis_ang[1], axis_ang[2])

def show_pid_acc(info):
    p_acc = info['p_axis_angle_acc']
    print 'p acc: x: %.2f  y: %.2f  z: %.2f' % (
            p_acc[0], p_acc[1], p_acc[2])

    i_acc = info['i_axis_angle_acc']
    print 'i acc: x: %.2f  y: %.2f  z: %.2f' % (
            i_acc[0], i_acc[1], i_acc[2])

    d_acc = info['d_axis_angle_acc']
    print 'd acc: x: %.2f  y: %.2f  z: %.2f' % (
            d_acc[0], d_acc[1], d_acc[2])

def show_para(info):
    max_acc = info['max_ang_acc']
    c_time = info['angle_velocity_catch_time']
    p = info['p']
    i = info['i']
    d = info['d']

    print 'max_ang_acc: %.2f  catch_time: %.2f  p: %.2f  i: %.2f  d: %.2f' % (
            max_acc, c_time, p, i, d)


def show_throttle_diff(info):
    print '------throttle diff-----'
    d = util.get_throttle_diff(info)
    print '%.2f %.2f %.2f' % (d[0], d[1], d[2])

def show_pwms(info):
    pwms = info['motor_pwms']
    print 'pwm: %d %d %d %d' % (pwms[0], pwms[1], pwms[2], pwms[3])

def show_power_volt(info):
    print 'power volt: %.2f ' % info['power_volt']


def show_info(info):
    print ''
    print '*********************'
    print 'tick: %.2f  control_n: %.2f' % (info['tick'], info['control_n'])

    show_angle(info)
    show_pid_acc(info)
    show_para(info)
    show_power_volt(info)
    show_pwms(info)

    print ''

def run(s):
    total_data = ''
    start = 0
    stop = 0

    while True:
        data, info = util.get_info(s)
        if info == 0:
            time.sleep(0.01)
            continue

        if info['lever_throttles'][2] > 90:
            if start == 0:
                print 'start recording'
                start = 1

        if info['lever_throttles'][0] < -80:
            if start == 1:
                stop = 1
                print 'stop recording'

        if stop == 1:
            break

        if start == 1:
            total_data += data

        show_info(info)

        time.sleep(0.005)

    f = open('data.txt', 'wb')
    f.write(total_data)
    f.close()
    print 'write %d bytes to data.txt' % len(total_data)

if __name__ == '__main__':
    s = util.connect()
    run(s)

    s.close() 
