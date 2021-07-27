import pyrr
import math
import pygame
import quaternion

class Camera:
    def __init__(self, view_point=None):
        if view_point is None:
            self.view_point = [0.0, 0.0, 5]
        else:
            self.view_point = view_point

        self.up_axis = [0.0, 1.0, 0.0]
        self.snap_view_point = self.view_point

        self.update_up_axis()

        self.update_view()

        self.mouse_down = False
        self.mouse_down_x = 0
        self.mouse_down_y = 0

        self.wheel_down = False
        self.wheel_down_x = 0
        self.wheel_down_y = 0

        self.mouse_x = 0
        self.mouse_y = 0

    def update_up_axis(self):
        if abs(self.snap_view_point[0]) + abs(self.snap_view_point[2]) < 0.1:
            self.up_axis = [1.0, 0.0, 0.0]

        right_axis = quaternion.cross(self.up_axis, self.snap_view_point)
        self.up_axis = quaternion.cross(self.snap_view_point, right_axis)

    def update_view(self):
        self.view = pyrr.matrix44.create_look_at(
                pyrr.Vector3(self.view_point),
                pyrr.Vector3([0.0, 0.0, 0.0]),
                self.up_axis)

    def update_view_point(self):
        if self.mouse_down:
            self.rotate()

        if self.wheel_down:
            self.scale()

        self.update_view()

    def rotate(self):
        dx = self.mouse_x - self.mouse_down_x
        dy = self.mouse_y - self.mouse_down_y

        angle_x = -dx / 10.0
        angle_y = -dy / 10.0

        right_axis = quaternion.cross(self.up_axis, self.snap_view_point)

        qx = quaternion.from_axis_angle(self.up_axis, angle_x)
        qy = quaternion.from_axis_angle(right_axis, angle_y)

        q = quaternion.multiply(qx, qy)

        v_len = quaternion.vector_len(self.snap_view_point)
        self.view_point = quaternion.rotate_vector(self.snap_view_point, q)
        self.view_point = quaternion.vector_scale(self.view_point, v_len)

    def scale(self):
        dy = self.mouse_y - self.wheel_down_y

        if dy >= 0:
            s = 1.0 + dy / 500.0
        else:
            s = 500.0 / (abs(dy) + 500.0)

        v = self.snap_view_point

        self.view_point = [v[0] * s, v[1] * s, v[2] * s]


    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_down = True
                self.mouse_down_x = event.pos[0]
                self.mouse_down_y = event.pos[1]
            if event.button == 2:
                self.wheel_down = True
                self.wheel_down_x = event.pos[0]
                self.wheel_down_y = event.pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down = False
            if event.button == 2:
                self.wheel_down = False

            self.snap_view_point = self.view_point
            self.update_up_axis()

        if event.type == pygame.MOUSEMOTION:
            self.mouse_x = event.pos[0]
            self.mouse_y = event.pos[1]
            self.update_view_point()


def test():
    pygame.init()
    pygame.display.set_mode((640, 480))


    camera_obj = Camera()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            camera_obj.process_event(event)

        pygame.display.flip()


if __name__ == '__main__':
    test()



