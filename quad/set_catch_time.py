import socket
import time
import struct
import util

catch_time = 0.1

def run(s):
    msg = '2' + struct.pack('<If', 3, catch_time) + '\r\n'
    s.send(msg)

    d = s.recv(100)
    if d != '0':
        print 'error: recv is: %s' % d

    print 'set angle velocity catch time to: %f' % catch_time

if __name__ == '__main__':
    s = util.connect()
    run(s)

    s.close() 
