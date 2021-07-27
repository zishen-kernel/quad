import util
from matplotlib import pyplot as plt

def load_data(file_name):
    f = open(file_name, 'rb')
    total_data = f.read()
    f.close()

    bytes_n = len(total_data)
    info_n = bytes_n / 152

    infos = []
    for i in range(info_n):
        data = total_data[i*152: (i+1) * 152]
        info = util.unpack_info(data)
        infos.append(info)

    return infos

def calc_hz(infos):
    n = len(infos)
    start_tick = infos[0]['tick']
    end_tick = infos[n-1]['tick']

    time_ms = end_tick - start_tick

    hz = n / time_ms * 1000.0
    return hz

def run():
    infos = util.load_data('data.txt')
    hz = util.calc_hz(infos)
    diff_angle = util.get_diff_angle(infos)
    axis_diff_angle = util.get_axis_diff_angle(infos)
    pwms = util.get_pwm(infos)
    gyro = util.get_gyro(infos)
    angle_velocity = util.get_angle_velocity(infos)
    data_fusion_q = util.get_data_fusion_q(infos)

    for i in range(50, 60):
        print i
        print infos[i]['data_fusion_q']
        print infos[i]['dst_q']
        print infos[i]['q_diff_local_axis_normal']
    #plt.plot(gyro[0], 'ro')
    #plt.plot(angle_velocity[0], 'bo')
    plt.plot(axis_diff_angle[0], 'go')
    plt.show()

if __name__ == '__main__':
    run()
