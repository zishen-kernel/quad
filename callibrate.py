import pickle
import numpy
import math

def run():
    fd = open('sensor_data.txt', 'rb')
    mag = pickle.load(fd)
    mag = mag[:1000]

    mat = []
    for m in mag:
        mat.append(m[0] * m[0])
        mat.append(m[0])
        mat.append(m[1] * m[1])
        mat.append(m[1])
        mat.append(m[2] * m[2])
        mat.append(m[2])

    Mat = numpy.array(mat).reshape(1000, 6)

    Mat_tran = Mat.transpose()

    Mat_mul = Mat_tran.dot(Mat)

    Mat_inv = numpy.linalg.inv(Mat_mul)

    B = numpy.array([1.0] * 1000)
    tran_B = Mat_tran.dot(B)

    X = Mat_inv.dot(tran_B)

    rt = 1.0 + (X[1] * X[1])/(4.0 * X[0]) + \
              (X[3] * X[3])/(4.0 * X[2]) + \
              (X[5] * X[5])/(4.0 * X[4])


    rx = math.sqrt(rt / X[0])
    ry = math.sqrt(rt / X[2])
    rz = math.sqrt(rt / X[4])

    offx = -X[1] / (2.0 * X[0])
    offy = -X[3] / (2.0 * X[2])
    offz = -X[5] / (2.0 * X[4])

    print '%.3f, %.3f, %.3f' % (rx, ry, rz)
    print '%.3f, %.3f, %.3f' % (offx, offy, offz)

    calli_mag = []

    for m in mag:
        calli_m = [m[0] - offz, m[1] - offy, m[2] - offz]
        calli_m = [calli_m[0] / rx, calli_m[1] / ry, calli_m[2] / rz]

        calli_mag.append(calli_m)


    fd = open('calli_data.txt', 'wb')
    pickle.dump(calli_mag, fd)

if __name__ == '__main__':
    run()
