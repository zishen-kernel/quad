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
    for i in infos:
        print i['mag_acc_quality']
    return
    volts = util.get_power_volt(infos)
    hz = util.calc_hz(infos)
    diff_angle = util.get_diff_angle(infos)
    axis_diff_angle = util.get_axis_diff_angle(infos)
    pwms = util.get_pwm(infos)
    gyro = util.get_gyro(infos)
    angle_velocity = util.get_angle_velocity(infos)
    data_fusion_q = util.get_data_fusion_q(infos)
    lever_throttles = util.get_lever_throttles(infos)
    throttle_diff = util.get_throttle_diff(infos)
    
    #plt.plot(pwms[0], 'bo')
    #plt.plot(pwms[1], 'ro')
    #plt.plot(pwms[2], 'ro')
    #plt.plot(pwms[3], 'bo')
    plt.plot(axis_diff_angle[0], 'ro')
    plt.plot(axis_diff_angle[1], 'go')
    plt.plot(axis_diff_angle[2], 'bo')
    #plt.plot(angle_velocity[0])
    #plt.plot(gyro[0], 'ro')
    #plt.plot(throttle_diff[0], 'bo')
    #plt.plot(volts, 'ro')
    plt.show()

if __name__ == '__main__':
    run()
