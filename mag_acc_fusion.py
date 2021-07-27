import quaternion
import math
from matplotlib import pyplot as plt
import pickle

class MagAccFusion:
    def __init__(self):
        self.q = [1.0, 0.0, 0.0, 0.0]
        self.angle = 50.0 / 180.0 * math.pi
        self.mag_vector = [math.cos(self.angle), 0.0, -math.sin(self.angle)]
        self.quality = 0.0

    def neg_q(self, q):
        q_neg = []
        q_neg.append(q[0])
        q_neg.append(-q[1])
        q_neg.append(-q[2])
        q_neg.append(-q[3])

        return q_neg

    def neg_v(self, v):
        v_neg = []
        v_neg.append(-v[0])
        v_neg.append(-v[1])
        v_neg.append(-v[2])

        return v_neg


    def fuse(self, mag_normal, acc):
        acc_len = quaternion.vector_len(acc)
        if acc_len < 0.95 or acc_len > 1.05:
            self.quality = 0.0
            return

        acc_normal = quaternion.normal(acc)
        mag_rot_q = quaternion.from_two_vector(self.mag_vector, mag_normal)

        gravity_vector = self.neg_v(acc_normal)

        origin_gravity = quaternion.rotate_vector([0.0, 0.0, -1.0], mag_rot_q)

        v1 = quaternion.cross(mag_normal, gravity_vector)
        v2 = quaternion.cross(mag_normal, origin_gravity)

        v1 = quaternion.normal(v1)
        v2 = quaternion.normal(v2)

        ang_rot_dot = quaternion.dot(v1, v2)
        ang_rot = math.acos(ang_rot_dot) * 180.0 / math.pi

        v_axis = quaternion.cross(v2, v1)
        v_axis = quaternion.normal(v_axis)

        ang_axis_dot = quaternion.dot(v_axis, mag_normal)
        if ang_axis_dot <= -1.0:
            ang_axis_dot = -0.99999
        if ang_axis_dot >= 1.0:
            ang_axis_dot = 0.99999

        ang_axis = math.acos(ang_axis_dot) * 180.0 / math.pi

        rot_axis = mag_normal

        if ang_axis > 90.0:
            rot_axis = self.neg_v(mag_normal)

        rot_q = quaternion.from_axis_angle(rot_axis, ang_rot)

        rot_gravity = quaternion.rotate_vector(origin_gravity, rot_q)

        dot = quaternion.dot(rot_gravity, gravity_vector)
        ang = math.acos(dot) * 180.0 / math.pi

        quality = ang / 10.0
        if quality > 1.0:
            quality = 1.0

        self.quality = quality

        #print '%.2f %.2f %.2f %.2f' % (ang2, ang_axis, ang_rot, ang)

        q = quaternion.multiply(rot_q, mag_rot_q)

        self.q = self.neg_q(q)
