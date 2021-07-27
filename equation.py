import quaternion
import math

def calc_error(x_axis, y_axis, z_axis):
    e1 = quaternion.dot(x_axis, y_axis)
    e1 = abs(e1)

    e2 = quaternion.dot(y_axis, z_axis)
    e2 = abs(e2)

    e3 = quaternion.dot(x_axis, z_axis)
    e3 = abs(e3)

    z = quaternion.cross(x_axis, y_axis)
    e4 = quaternion.cross(z, z_axis)
    e4 = quaternion.vector_len(e4)

    dot4 = quaternion.dot(z, z_axis)
    if dot4 < 0.3:
        e4 += 2.0


    e = e1 + e2 + e3 + e4
    return e

def select_axis(xs, ys, zs):
    combines = []
    errors = []

    for x_axis in xs:
        for y_axis in ys:
            for z_axis in zs:
                combines.append([x_axis, y_axis, z_axis])
                e = calc_error(x_axis, y_axis, z_axis)
                errors.append(e)

    min_error = 100.0
    min_index = 0
    for i in range(len(errors)):
        if errors[i] < min_error:
            min_error = errors[i]
            min_index = i


    #print errors[min_index]
    return combines[min_index]

# a is axis x cord
# b is axis y cord
# m is the cos 
# y is the gravity acc
def calc_axis(a, b, m, y):
    ra = -(a * a + b * b)
    rb = 2.0 * m * b
    rc = a * a - m * m

    eq_y = ra * y * y + rb * y + rc

    if eq_y > 0:
        z1 = math.sqrt(eq_y / (a * a))
        z2 = -math.sqrt(eq_y / (a * a))

        x = (m - b * y) / a

        return [[x, y, z1], [x, y, z2]]

    elif eq_y == 0:
        z = 0.0
        x = (m - b * y) / a

        return [[x, y, z]]

    else:
        z = 0.0
        delta = rb * rb - 4.0 * ra * rc
        if delta < 0.0:
            print 'error, delta < 0'
        else:
            y1 = (-rb + math.sqrt(delta)) / (2.0 * ra)
            y2 = (-rb - math.sqrt(delta)) / (2.0 * ra)
            x1 = (m - b * y1) / a
            x2 = (m - b * y2) / a
            if abs(y1 - y) < (y2 - y):
                return [[x1, y1, z]]
            else:
                return [[x2, y2, z]]


def test():
    r = calc_error([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0])



if __name__ == '__main__':
    test()
