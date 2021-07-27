import socket
import time
import struct
import get_info

max_acc = 800

def run(s):
    msg = '2' + struct.pack('<If', 2, max_acc) + '\r\n'
    s.send(msg)

    d = s.recv(100)
    if d != '0':
        print 'error: recv is: %s' % d

    print 'set max angle acc to: %f' % max_acc

if __name__ == '__main__':
    s = get_info.connect()
    run(s)

    s.close() 
