
def acc_adjust(acc):
    x, y, z = acc
    new_acc = [y, -x, z]

    xx, yy, zz = new_acc

    xx = 4.0 * xx / 32768.0
    yy = 4.0 * yy / 32768.0
    zz = 4.0 * zz / 32768.0

    if xx < 0:
        xx = xx / 1.01
    else:
        xx = xx / 1.00

    if yy < 0:
        yy = yy / 1.03
    else:
        yy = yy / 0.98

    if zz < 0:
        zz = zz / 1.03
    else:
        zz = zz / 1.02

    #print '%.3f %.3f %.3f' % (xx, yy, zz)

    return [xx, yy, zz]
