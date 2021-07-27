import socket
import time
import struct
import util

curr_pwm = 2 

def run(s):
    msg = '2' + struct.pack('<II', 7, curr_pwm) + '\r\n'
    s.send(msg)

    data = s.recv(100)
    if data != '0':
        print 'error: recv is: %s' % data

    print 'set curr_pwm to: %d' % curr_pwm

if __name__ == '__main__':
    s = util.connect()
    run(s)

    s.close() 
