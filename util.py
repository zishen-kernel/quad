import struct
import socket


def unpack_info(data):
    r = struct.unpack('f' * 60, data)

    info = {}
    info['tick'] = r[0]
    r = r[1:]

    info['control_n'] = r[0]
    r = r[1:]

    info['power_volt'] = r[0]
    r = r[1:]

    info['data_fusion_q'] = r[:4]
    r = r[4:]

    info['dst_q'] = r[:4]
    r = r[4:]

    info['q_diff'] = r[:4]
    r = r[4:]

    info['mag_acc_q'] = r[:4]
    r = r[4:]

    info['acc'] = r[:3]
    r = r[3:]

    info['gyro'] = r[:3]
    r = r[3:]

    info['q_diff_angle'] = r[0]
    r = r[1:]

    info['q_diff_local_axis_normal'] = r[:3]
    r = r[3:]

    info['max_ang_acc'] = r[0]
    r = r[1:]

    info['axis_angle_velocity'] = r[:3]
    r = r[3:]

    info['angle_velocity_catch_time'] = r[0]
    r = r[1:]

    info['p_axis_angle_acc'] = r[:3]
    r = r[3:]

    info['i_axis_angle_acc'] = r[:3]
    r = r[3:]

    info['d_axis_angle_acc'] = r[:3]
    r = r[3:]

    info['p'] = r[0]
    r = r[1:]

    info['i'] = r[0]
    r = r[1:]

    info['d'] = r[0]
    r = r[1:]

    info['axis_moment'] = r[:3]
    r = r[3:]

    info['throttle_diff'] = r[:3]
    r = r[3:]

    info['motor_pwms'] = r[:4]
    r = r[4:]

    info['lever_throttles'] = r[:4]
    r = r[4:]

    return info


def load_data(file_name):
    f = open(file_name, 'rb')
    total_data = f.read()
    f.close()

    info_len = 240

    bytes_n = len(total_data)
    info_n = bytes_n / info_len

    infos = []
    for i in range(info_n):
        data = total_data[i*info_len: (i+1) * info_len]
        info = unpack_info(data)
        infos.append(info)

    return infos

def calc_hz(infos):
    n = len(infos)
    start_tick = infos[0]['tick']
    end_tick = infos[n-1]['tick']

    time_ms = end_tick - start_tick

    hz = n / time_ms * 1000.0
    return hz

def get_power_volt(infos):
    if type(infos) == dict:
        return infos['power_volt']

    volts = []
    for i in range(len(infos)):
        volts.append(infos[i]['power_volt'])

    return volts

def get_diff_angle(infos):
    if type(infos) == dict:
        return infos['q_diff_angle']

    diff_angle = []
    for i in range(len(infos)):
        diff_angle.append(infos[i]['q_diff_angle'])

    return diff_angle

def get_axis_diff_angle(infos):
    if type(infos) == dict:
        ang = infos['q_diff_angle']
        axis = infos['q_diff_local_axis_normal']
        return [ang * axis[0], ang * axis[1], ang * axis[2]]

    axis_diff_angle = [[], [], []]

    for i in range(len(infos)):
        diff_angle = infos[i]['q_diff_angle']
        axis = infos[i]['q_diff_local_axis_normal']
        for j in range(3):
            axis_diff_angle[j].append(diff_angle * axis[j])

    return axis_diff_angle

def get_throttle_diff(infos):
    if type(infos) == dict:
        th = infos['throttle_diff']
        return [th[0], th[1], th[2]]

    th_diff = [[], [], []]

    for i in range(len(infos)):
        th = infos[i]['throttle_diff']
        for j in range(3):
            th_diff[j].append(th[j])

    return th_diff

def get_lever_throttles(infos):
    if type(infos) == dict:
       th = infos['lever_throttles']

    ths = [[], [], [], []]
    for i in range(len(infos)):
        th = infos[i]['lever_throttles']
        for j in range(4):
            ths[j].append(th[j])

    return ths

def get_pwm(infos):
    pwms = [[], [], [], []]

    for i in range(len(infos)):
        motor_pwms = infos[i]['motor_pwms']
        for j in range(4):
            pwms[j].append(motor_pwms[j])

    return pwms

def get_gyro(infos):
    gyro = [[], [], []]

    for i in range(len(infos)):
        g = infos[i]['gyro']
        for j in range(3):
            gyro[j].append(g[j])

    return gyro

def get_angle_velocity(infos):
    angle_velocity = [[], [], []]

    for i in range(len(infos)):
        v = infos[i]['axis_angle_velocity']
        for j in range(3):
            angle_velocity[j].append(v[j])

    return angle_velocity

    

def get_data_fusion_q(infos):
    if type(infos) is dict:
        return infos['data_fusion_q']

    qs = []

    for i in range(len(infos)):
        qs.append(infos[i]['data_fusion_q'])

    return qs

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'start to connect'
    s.connect(('192.168.4.1', 3333))
    print 'connection: %s' % s
    return s

def get_info(s):
    s.send('1\r\n')
    data = s.recv(300)

    if len(data) == 1:
        return '0', 0

    if len(data) != 240:
        print 'error: data len is %d' % len(data)

    info = unpack_info(data)

    return data, info
