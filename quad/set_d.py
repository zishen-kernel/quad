import socket
import time
import struct
import util

d = 0.1

def run(s):
    msg = '2' + struct.pack('<If', 5, d) + '\r\n'
    s.send(msg)

    data = s.recv(100)
    if data != '0':
        print 'error: recv is: %s' % data

    print 'set d to: %f' % d

if __name__ == '__main__':
    s = util.connect()
    run(s)

    s.close() 
