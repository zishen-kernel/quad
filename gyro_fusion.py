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
import control

class GyroFusion:
    def __init__(self):
        self.mag_acc_fusion_obj = mag_acc_fusion.MagAccFusion()
        self.q = None

        self.gyro_init_q = None
        self.gyro_diff_q = [1.0, 0.0, 0.0, 0.0]

        self.adjust_q = None


    def fuse(self, gyro_q, mag_normal, acc):
        self.mag_acc_fusion_obj.fuse(mag_normal, acc)

        if self.q is None:
            self.gyro_init_q = gyro_q
            self.adjust_q = self.mag_acc_fusion_obj.q

        self.gyro_diff_q = quaternion.diff(self.gyro_init_q, gyro_q) 

        new_q = quaternion.multiply(self.adjust_q, self.gyro_diff_q)

        diff_q = quaternion.diff(new_q, self.mag_acc_fusion_obj.q)
        diff_q = quaternion.standardize(diff_q)

        step_adj_q = quaternion.scale(diff_q, self.mag_acc_fusion_obj.quality / 20.0)

        self.adjust_q = quaternion.multiply(step_adj_q, self.adjust_q)

        self.q = quaternion.multiply(self.adjust_q, self.gyro_diff_q)

        control.control(self.q)

