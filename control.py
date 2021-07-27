import quaternion

def control(q):
    dest_q = [1.0, 0.0, 0.0, 0.0]
    dest_q = quaternion.from_axis_angle([1.0, 0.0, 0.0], 90)

    error_q = quaternion.diff(q, dest_q)
    error_q = quaternion.standardize(error_q)

    error_q_axis, error_q_angle = quaternion.get_axis_angle(error_q)

    rotate_q = quaternion.neg(q)

    body_error_q_axis = quaternion.rotate_vector(error_q_axis, rotate_q)

    x_angle = error_q_angle * body_error_q_axis[0]
    y_angle = error_q_angle * body_error_q_axis[1]
    z_angle = error_q_angle * body_error_q_axis[2]

    print '%.2f %.2f %.2f' % (x_angle, y_angle, z_angle)


def run1(accx, accy, accz):
    v_acc = [accx, accy, accz]
    v_dest = [0.0, 0.0, 1.0]

    q = quaternion.from_two_vector(v_acc, v_dest)

    axis, angle = quaternion.get_axis_angle(q)

    x_error = angle * q[1]
    y_error = angle * q[2]

    #print "%.2f   %.2f" % (x_error, y_error)

    s1, s2, s3, s4 = 0, 0, 0, 0

    s2 += y_error
    s3 += y_error
    s1 -= y_error
    s4 -= y_error

    s3 += x_error
    s4 += x_error
    s1 -= x_error
    s2 -= x_error

    print "%.2f %.2f %.2f %.2f" % (s1, s2, s3, s4)

