#!/usr/bin/env python2

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 1234
BUFFER_SIZE = 98  # Normally 1024, but we want fast response


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()

try:
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if data:
            print "received data: ", data

finally:
    conn.close()
    print("Con closed!")