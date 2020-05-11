import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
hostIP = socket.gethostbyname(host)
s.bind((hostIP, 1234))
s.listen(5)
print(host)
print(hostIP)
print(s)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
