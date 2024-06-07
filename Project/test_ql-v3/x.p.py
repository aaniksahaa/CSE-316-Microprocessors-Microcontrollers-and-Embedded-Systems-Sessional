import socket
import time

s = socket.socket()
s.connect(('192.168.154.131',81))

while True:
    s.send("w".encode())
    time.sleep(1)
    print("w")