
mag_max = [0.14877, 0.155243, 0.18402]
mag_min = [-0.24292, -0.2294, -0.202179]

x_max = [0.0, 0.0]
y_max = [0.0, 0.0]
z_max = [0.0, 0.0]


def get_max(mag):
    if mag[0] < x_max[0]:
        x_max[0] = mag[0]

    if mag[0] > x_max[1]:
        x_max[1] = mag[0]

    if mag[1] < y_max[0]:
        y_max[0] = mag[1]

    if mag[1] > y_max[1]:
        y_max[1] = mag[1]

    if mag[2] < z_max[0]:
        z_max[0] = mag[2]

    if mag[2] > z_max[1]:
        z_max[1] = mag[2]
    

def mag_adjust(mag):

    for i in range(3):
        mag[i] = mag[i] / 32768.0

    get_max(mag)

    for i in range(3):

        if mag[i] >= 0:
            mag[i] = mag[i] / mag_max[i]
        else:
            mag[i] = -mag[i] / mag_min[i]
