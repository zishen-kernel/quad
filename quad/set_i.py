import socket
import time
import struct
import util

i = 0.01

def run(s):
    msg = '2' + struct.pack('<If', 5, i) + '\r\n'
    s.send(msg)

    d = s.recv(100)
    if d != '0':
        print 'error: recv is: %s' % d

    print 'set i to: %f' % i

if __name__ == '__main__':
    s = util.connect()
    run(s)

    s.close() 
