import socket
import time

headerSize = 8
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
hostIP = socket.gethostbyname(host)
s.bind((hostIP, 561))
s.listen(5)
print(host)
print(hostIP)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    message = "Connection established!"
    message = f"{len(message):<{headerSize}}" + message
    clientsocket.send(bytes(message, "utf-8"))

    while True:
        time.sleep(3)
        message = f"Current time: {time.time()}"
        message = f"{len(message):<{headerSize}}" + message

        print(message)

        clientsocket.send(bytes(message, "utf-8"))
