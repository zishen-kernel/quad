from matplotlib import pyplot as plt
import math


class Tda:
    def __init__(self, r=2.0, steps=100):
        self.origin_r = r
        self.r = self.origin_r
        self.steps = steps
        self.h = 1.0 / self.steps

        self.x1 = 0.0
        self.x2 = 0.0

    def fhan(self, v):
        fh = 0.0
        self.d = self.r * self.h
        self.d0 = self.d * self.h
        self.y = self.x1 - v + self.h * self.x2

        a0 = math.sqrt(self.d * self.d + 8.0 * self.r * abs(self.y))

        if abs(self.y) > self.d0:
            a = self.x2 + (a0 - self.d) / 2.0 * self.y / abs(self.y)
        else:
            a = self.x2 + self.y / self.h

        if abs(a) > self.d:
            fh = -self.r * a / abs(a)
        else:
            fh = -self.r * a / self.d

        return fh

    def trace(self, v):
        x2s = []
        x1s = []

        for i in range(self.steps):
            fh = self.fhan(v)
            self.x2 += fh * self.h
            self.x1 += self.x2 * self.h

            x2s.append(self.x2)
            x1s.append(self.x1)

        return self.x1

class Tdc:
    def __init__(self):
        self.fast_td = Tda(r=0.01)
        self.slow_td = Tda(r=0.0001)

        self.second_td = Tda(r=0.1)

    def trace(self, v):
        fast_x1 = self.fast_td.trace(v)
        slow_x1 = self.slow_td.trace(v)

        diff = abs(fast_x1 - slow_x1)

        if fast_x1 - slow_x1 > 0.05:
            rate = (diff - 0.05) / 0.04
            if rate > 1.0:
                rate = 1.0
            slow_x1 = fast_x1 - 0.05 * (1.0 - rate)
            self.slow_td.x1 = slow_x1
            self.slow_td.x2 = 0

        if fast_x1 - slow_x1 < -0.05:
            rate = (diff - 0.05) / 0.04
            if rate > 1.0:
                rate = 1.0
            slow_x1 = fast_x1 + 0.05 * (1.0 - rate)
            self.slow_td.x1 = slow_x1
            self.slow_td.x2 = 0

        r = 0.0
        if abs(fast_x1 - slow_x1) < 0.05:
            r = slow_x1

        else:
            rate = (diff - 0.05) / 0.02
            if rate > 1.0:
                rate = 1.0

            r = slow_x1 * (1.0 - rate) + fast_x1 * rate

        #r = self.second_td.trace(r)
        return r

def test():
    td = Tda(8)
    td.trace(1.0)

if __name__ == '__main__':
    test()
