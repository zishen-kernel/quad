import socket
import time
import struct
import util

p = 2.0

def run(s):
    msg = '2' + struct.pack('<If', 4, p) + '\r\n'
    s.send(msg)

    d = s.recv(100)
    if d != '0':
        print 'error: recv is: %s' % d

    print 'set p to: %f' % p

if __name__ == '__main__':
    s = util.connect()
    run(s)

    s.close() 
