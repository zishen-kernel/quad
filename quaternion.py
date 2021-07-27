import math
import numpy
import pyrr

def q_to_matrix(q):
    axis, rad = get_axis_angle(q, radians=True)
    mat = pyrr.matrix44.create_from_axis_rotation(
            pyrr.Vector3(axis), rad)

    return mat


def standardize(q):
    stand_q = [0.0] * 4

    for i in range(4):
        if q[0] < 0:
            stand_q[i] = -q[i]
        else:
            stand_q[i] = q[i]

    return stand_q

def get_axis_angle(q, radians=False):
    if q[0] >= 1.0:
        return [1.0, 0.0, 0.0], 0.0

    axis = q[1:4]

    rad = math.acos(q[0]) * 2.0

    if radians is True:
        return axis, rad

    angle = rad / math.pi * 180.0

    return axis, angle


def from_axis_angle(aixs, angle):
    aixs = pyrr.vector3.normalize(aixs)
    rad = numpy.radians(angle)

    c = math.cos(rad / 2.0)
    s = math.sin(rad / 2.0)
    q = [ c ]

    q.extend((aixs * s).tolist())

    return q

def cross(v1, v2):
    ai, aj, ak = v1
    bi, bj, bk = v2

    pi = aj * bk - ak * bj
    pj = ak * bi - ai * bk
    pk = ai * bj - aj * bi

    return [pi, pj, pk]

def dot(v1, v2):
    ai, aj, ak = v1
    bi, bj, bk = v2
    dot = ai * bi + aj * bj + ak * bk

    return dot

def vector_len(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])

def q_len(q):
    return math.sqrt(q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3])

def angle(v1, v2):
    ai, aj, ak = v1
    bi, bj, bk = v2

    lena = math.sqrt(ai * ai + aj * aj + ak * ak)
    lenb = math.sqrt(bi * bi + bj * bj + bk * bk)

    dot = ai * bi + aj * bj + ak * bk

    cos = dot / (lena * lenb)

    if cos > 1.0:
        print 'cos is > 1.0: %f' % cos
        cos = 1.0

    ang_radians = math.acos(cos)

    ang = 180.0 * ang_radians / math.pi

    return ang

def from_two_vector(v1, v2):
    axis = cross(v1, v2)
    ang = angle(v1, v2)

    return from_axis_angle(axis, ang)

def q_normal(q):
    m = q_len(q)

    normal_q = [0.0] * 4

    for i in range(4):
        normal_q[i] = q[i] / m

    return normal_q

def multiply(q_left, q_right):
    q1 = q_left
    q2 = q_right

    q = [0] * 4

    q[0] = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]

    q[1] = q1[0] * q2[1] + q2[0] * q1[1] + q1[2] * q2[3] - q2[2] * q1[3]

    q[2] = q1[0] * q2[2] + q2[0] * q1[2] + q1[3] * q2[1] - q2[3] * q1[1]

    q[3] = q1[0] * q2[3] + q2[0] * q1[3] + q1[1] * q2[2] - q2[1] * q1[2]

    return q_normal(q)


def diff(q_left, q_right):
    neg_left = [q_left[0]]
    neg_left.extend((pyrr.Vector3(q_left[1:]) * -1.0).tolist())

    #q_diff = multiply(neg_left, q_right)
    q_diff = multiply(q_right, neg_left)

    return q_diff

def scale(q, f):
    axis, angle = get_axis_angle(q)

    new_angle = angle * f 

    q = from_axis_angle(axis, new_angle)

    return q

def vector_scale(v, f):
    vs = []
    for i in range(len(v)):
        vs.append(v[i] * f)

    return vs

def neg(q):
    neg_q = [q[0]]
    neg_q.extend((pyrr.Vector3(q[1:]) * -1.0).tolist())

    return neg_q

def rotate(qv, q):
    neg_q = [q[0]]
    neg_q.extend((pyrr.Vector3(q[1:]) * -1.0).tolist())
    qr = multiply(qv, neg_q)
    qr = multiply(q, qr)

    return qr

def rotate_vector(v, q):
    qv = [0.0, v[0], v[1], v[2]]

    qr = rotate(qv, q)

    return qr[1:]

def normal(v):
    return pyrr.vector3.normalize(v).tolist()

def q_to_axis(q):
    x_axis = rotate_vector([1.0, 0.0, 0.0], q)
    y_axis = rotate_vector([0.0, 1.0, 0.0], q)
    z_axis = rotate_vector([0.0, 0.0, 1.0], q)

    return x_axis, y_axis, z_axis

def axis_to_q(x_axis, y_axis):
    if x_axis == [1.0, 0.0, 0.0]:
        q1 = [1.0, 0.0, 0.0, 0.0]
    else:
        q1 = from_two_vector([1.0, 0.0, 0.0], x_axis)

    v_y = rotate_vector([0.0, 1.0, 0.0], q1)

    if v_y == y_axis:
        q2 = [1.0, 0.0, 0.0, 0.0]
    else:
        q2 = from_two_vector(v_y, y_axis)

    q = multiply(q2, q1)


    return q

def test_q_axis():
    x = [0.9487887249155023, -0.035980540329145924, -0.3138556295350429]

    y = [-0.0693827948913147, -0.010757068758198266, -0.9975321113852933]

    print dot(x, y)

    q = axis_to_q(x, y)

    x, y, z = q_to_axis(q)




def test_from_two_vector():
    v1 = normal([1, 0, 0])
    v2 = normal([1, -0.01, 0])

    q = from_two_vector(v1, v2)

    axis, angle = get_axis_angle(q)

def test_multiply():
    q1 = from_axis_angle([1, 0, 0], 90)
    q2 = from_axis_angle([0, 1, 0], 90)

    print q1
    print q2

    x1 = rotate_vector([1.0, 0.0, 0.0], q1)
    print x1
    x2 = rotate_vector(x1, q2)
    print x2


    q = multiply(q2, q1)

    x22 = rotate_vector([1.0, 0.0, 0.0], q)



if __name__ == '__main__':
    #test_from_two_vector()
    test_q_axis()
    #test_multiply()

