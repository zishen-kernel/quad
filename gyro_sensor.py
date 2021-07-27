import quaternion

def gyro_adjust(gyro, q):
    x, y, z = gyro

    x = x / 32768.0 * 1000.0 + 4.027
    y = y / 32768.0 * 1000.0 - 2.621
    z = z / 32768.0 * 1000.0 - 0.79

    new_gyro = [y, -x, z]

    new_q = [q[0], q[2], -q[1], q[3]]

    return new_gyro, new_q
