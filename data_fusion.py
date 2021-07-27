import quaternion
import mag_sensor
import acc_sensor
import gyro_sensor
import td
import math
import equation
import mag_fusion
import mag_acc_fusion
import step_fusion
import gyro_fusion

class Fusion:
    def __init__(self):
        self.mag_fusion_obj = mag_fusion.MagFusion()
        self.mag_acc_fusion_obj = mag_acc_fusion.MagAccFusion()
        self.gyro_fusion_obj = gyro_fusion.GyroFusion()
        self.step_fusion_obj = step_fusion.StepFusion()
        self.gyro_q = [1.0, 0.0, 0.0, 0.0]
        self.calced_q = [1.0, 0.0, 0.0, 0.0]
        self.adjusted_q = None
        self.adjusted_gyro_q = None
        self.init_gyro_q = None
        self.mag = None
        self.acc = None
        self.acc_normal = None
        self.mag_normal = None
        self.gyro = None
        self.q = None
        self.mag_td_x = td.Tdc()
        self.mag_td_y = td.Tdc()
        self.mag_td_z = td.Tdc()

        self.mag_v = None

        self.mag_origin = None
        self.mag_acc_axis = None
        self.adjusted_axis = None
        self.gyro_axis = None
        self.mag_acc_init_q = None
        self.diff_q = None
        self.gyro_sync_q = None

    def feed(self, data):
        self.gyro_q = data['gyro_q']
        self.acc = data['acc']
        self.gyro = data['gyro']
        self.mag = data['mag']

        self.fuse()

    def trace(self):
        mag_x = self.mag_td_x.trace(self.mag[0])
        mag_y = self.mag_td_y.trace(self.mag[1])
        mag_z = self.mag_td_z.trace(self.mag[2])

        self.mag = [mag_x, mag_y, mag_z]

    def get_mag_v(self):
        x = self.mag_normal[0]
        y = self.mag_normal[1]
        z = self.mag_normal[2]

        xy = math.sqrt(x * x + y * y)

        mag_v = [xy, -abs(z), 0.0]

        return mag_v

    def adjust_axis(self):
        x_axis, y_axis, z_axis = self.mag_acc_axis

        x_x = x_axis
        x_z = quaternion.cross(x_x, y_axis)
        x_y = quaternion.cross(x_z, x_x)

        y_y = y_axis
        y_x = quaternion.cross(y_y, z_axis)
        y_z = quaternion.cross(y_x, y_y)

        z_z = z_axis
        z_y = quaternion.cross(z_z, x_axis)
        z_x = quaternion.cross(z_y, z_z)

        vs = [abs(self.mag[0]), abs(self.mag[1]), abs(self.mag[2])]
        v_min = min(vs)

        if v_min == vs[0]:
            return [x_x, x_y, x_z]
        if v_min == vs[1]:
            return [y_x, y_y, y_z]
        if v_min == vs[2]:
            return [z_x, z_y, z_z]

    def calc_axis(self):
        xs = equation.calc_axis(self.mag_v[0], self.mag_v[1],
                self.mag_normal[0], self.acc_normal[0])
        ys = equation.calc_axis(self.mag_v[0], self.mag_v[1],
                self.mag_normal[1], self.acc_normal[1])
        zs = equation.calc_axis(self.mag_v[0], self.mag_v[1],
                self.mag_normal[2], self.acc_normal[2])
    
        self.mag_acc_axis = equation.select_axis(xs, ys, zs)

        self.adjusted_axis = self.adjust_axis()

        if self.mag_acc_init_q is None:
            self.mag_acc_init_q = quaternion.axis_to_q(
                    self.adjusted_axis[0], self.adjusted_axis[1])

        if self.mag_acc_init_q is not None:
            self.gyro_sync_q = quaternion.multiply(self.mag_acc_init_q,
                    self.diff_q)

            self.gyro_axis = quaternion.q_to_axis(self.gyro_sync_q)

    def calc_q(self):
        x, y, z = self.adjusted_gyro

        v = [x, y, z]
        len_v = quaternion.vector_len(v)
        angle = len_v * 0.03

        v1 = quaternion.rotate_vector(v, self.calced_q)

        q = quaternion.from_axis_angle(v1, angle)

        self.calced_q = quaternion.multiply(q, self.calced_q)

        q = self.calced_q
        self.adjusted_q = [q[0], q[2], -q[1], q[3]]

    def fuse(self):
        mag_sensor.mag_adjust(self.mag)
        self.acc = acc_sensor.acc_adjust(self.acc)
        self.adjusted_gyro, self.adjusted_gyro_q = gyro_sensor.gyro_adjust(
                self.gyro, self.gyro_q)


        if self.init_gyro_q is None:
            self.init_gyro_q = self.adjusted_gyro_q

        self.diff_q = quaternion.diff(self.init_gyro_q, self.adjusted_gyro_q)

        #self.trace()

        self.mag_normal = quaternion.normal(self.mag)
        self.acc_normal = quaternion.normal(self.acc)

        self.gyro_fusion_obj.fuse(self.adjusted_gyro_q, self.mag_normal, self.acc)

        self.q = self.gyro_fusion_obj.q
