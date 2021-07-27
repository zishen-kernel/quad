import quaternion
import math
from matplotlib import pyplot as plt
import pickle

class MagFusion:
    def __init__(self):
        self.count = 0
        self.snap_count = None
        self.snap_mag = None
        self.snap_gyro_q = None
        self.gyro_diff = None
        self.count_diff = None
        self.need_calc = False
        self.q = [1.0, 0.0, 0.0, 0.0]
        self.angle = 50.0 / 180.0 * math.pi
        self.mag_vector = [math.cos(self.angle), 0.0, -math.sin(self.angle)]
        self.snap_q = [1.0, 0.0, 0.0, 0.0]
        self.calced_q = [1.0, 0.0, 0.0, 0.0]
        self.es_list = []


    def take_snap(self, mag, gyro_q):
        if self.snap_mag is None:
            self.snap_count = self.count
            self.snap_mag = mag
            self.snap_gyro_q = gyro_q
            return

        gyro_diff = quaternion.diff(self.snap_gyro_q, gyro_q)
        axis, angle = quaternion.get_axis_angle(gyro_diff)

        if angle < 10:
            return

        self.count_diff = self.count - self.snap_count
        self.gyro_diff = gyro_diff
        self.need_calc = True

    def neg_q(self, q):
        q_neg = []
        q_neg.append(q[0])
        q_neg.append(-q[1])
        q_neg.append(-q[2])
        q_neg.append(-q[3])

        return q_neg

    def increace_q(self, gyro_q):
        q_diff = quaternion.diff(self.snap_q, gyro_q)
        self.increaced_q = quaternion.multiply(q_diff, self.calced_q)

    def filter_q(self):
        self.q = self.increaced_q 


    def fuse(self, mag, gyro_q):
        self.take_snap(mag, gyro_q)
        self.count += 1

        self.increace_q(gyro_q)
        self.filter_q()

        if self.need_calc == False:
            return

        q_mag = quaternion.from_two_vector(mag, self.mag_vector)
        gyro_diff_neg = self.neg_q(self.gyro_diff)

        es = []
        for i in range(360):
            q_rot = quaternion.from_axis_angle(self.mag_vector, i)
            q_mag_rot = quaternion.multiply(q_rot, q_mag)

            q_last = quaternion.multiply(gyro_diff_neg, q_mag_rot)

            x_axis = quaternion.rotate_vector([1.0, 0.0, 0.0], q_last)
            y_axis = quaternion.rotate_vector([0.0, 1.0, 0.0], q_last)
            z_axis = quaternion.rotate_vector([0.0, 0.0, 1.0], q_last)

            x_v = quaternion.dot(x_axis, self.mag_vector)
            y_v = quaternion.dot(y_axis, self.mag_vector)
            z_v = quaternion.dot(z_axis, self.mag_vector)

            e = 0.0
            e += abs(x_v - self.snap_mag[0])
            e += abs(y_v - self.snap_mag[1])
            e += abs(z_v - self.snap_mag[2])
            es.append(e)

        min_e = min(es)
        min_index = es.index(min_e)
        average = sum(es) / len(es)

        self.es_list.append(es)

        if len(self.es_list) > 30:
            #f = open('es_list', 'wb')
            #pickle.dump(self.es_list, f)
            print 'dumped'

        axis, angle = quaternion.get_axis_angle(self.gyro_diff)
        axis = quaternion.normal(axis)
        dot = quaternion.dot(axis, self.mag_vector)
        

        q_rot = quaternion.from_axis_angle(self.mag_vector, min_index)
        q_mag_rot = quaternion.multiply(q_rot, q_mag)

        if min_e < 0.03 and dot < 0.9:
            print 'updated'
            self.snap_q = gyro_q
            self.calced_q = q_mag_rot
        else:
            print 'not acurate'

        self.need_calc = False 
        self.snap_mag = None

