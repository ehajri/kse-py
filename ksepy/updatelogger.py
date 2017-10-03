import socket, sys, struct

with open('logging.conf', 'rb') as f:
    data_to_send = f.read()

HOST = 'localhost'
PORT = 44556
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('connecting...')
s.connect((HOST, PORT))
print('sending config...')
s.send(struct.pack('>L', len(data_to_send)))
s.send(data_to_send)
s.close()
print('complete')