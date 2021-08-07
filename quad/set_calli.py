import socket
import time
import struct
import util

offx = -0.226
offy = -0.296
offz = -0.310

rx = 1.009
ry = 1.026
rz = 1.048

def run(s):
    msg = '2' + struct.pack('<Iffffff', 8, offx, offy, offz, rx, ry, rz) + '\r\n'
    s.send(msg)

    data = s.recv(100)
    if data != '0':
        print 'error: recv is: %s' % data

    print 'set calli'

if __name__ == '__main__':
    s = util.connect()
    run(s)

    s.close() 
