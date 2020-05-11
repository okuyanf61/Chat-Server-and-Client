import socket

headerSize = 8
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
hostIP = socket.gethostbyname(host)
s.connect((socket.gethostname(), 561))
while True:
    fullMessage = ""
    newMessage = True
    while True:
        message = s.recv(32)
        if newMessage:
            messageLen = int(message[:headerSize])
            newMessage = False

        fullMessage += message.decode("utf-8")

        if len(fullMessage) - headerSize == messageLen:
            print(fullMessage[headerSize:])
            newMessage = True
            fullMessage = ""
