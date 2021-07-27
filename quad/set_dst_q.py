import socket
import time
import struct
import util

def run(s):
    data, info = get_info.get_info(s)
    data_fusion_q = info['data_fusion_q']

    q = data_fusion_q
    msg = '2' + struct.pack('<Iffff', 1, q[0], q[1], q[2], q[3]) + '\r\n'
    s.send(msg)

    d = s.recv(100)
    if d != '0':
        print 'error: recv is: %s' % d

    print 'set dst q to:'
    print data_fusion_q

if __name__ == '__main__':
    s = util.connect()
    run(s)

    s.close() 
