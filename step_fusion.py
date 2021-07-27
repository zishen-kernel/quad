import quaternion
import math
from matplotlib import pyplot as plt
import pickle

class StepFusion:
    def __init__(self):
        self.q = [1.0, 0.0, 0.0, 0.0]
        self.angle = 50.0 / 180.0 * math.pi
        self.mag_vector = [math.cos(self.angle), 0.0, -math.sin(self.angle)]


    def neg_q(self, q):
        q_neg = []
        q_neg.append(q[0])
        q_neg.append(-q[1])
        q_neg.append(-q[2])
        q_neg.append(-q[3])

        return q_neg


    def fuse(self, mag, gyro_q):
        dot = quaternion.dot(mag, self.mag_vector)
        ang = math.acos(dot)
        ang = ang * 180.0 / math.pi

        rotated_mag = quaternion.rotate_vector(self.mag_vector, gyro_q)

        dot2 = quaternion.dot(rotated_mag, self.mag_vector)
        ang2 = math.acos(dot2)
        ang2 = ang2 * 180.0 / math.pi
        print '%.2f  %.2f' % (ang, ang2)

