import socket
import errno
import sys
import argparse

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("-i", "--ip", required=True, help="IP Address")
argumentParser.add_argument("-p", "--port", required=True, help="Port")
args = vars(argumentParser.parse_args())

headerSize = 8

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostIP = args["ip"]
hostPort = int(args["port"])

try:
    server.connect((hostIP, hostPort))
except OSError as error:
    print("OS Error: " + str(error))
    sys.exit()

server.setblocking(False)

userName = input("What's your username? : ")
userName = userName.encode("utf-8")
userNameHeader = f"{len(userName):<{headerSize}}".encode('utf-8')

server.send(userNameHeader + userName)

while True:
    message = input(f'{userName.decode("utf-8")}: ')

    if message:
        message = message.encode("utf-8")
        messageHeader = f"{len(message):<{headerSize}}".encode("utf-8")
        server.send(messageHeader + message)

    try:
        while True:
            userNameHeader = server.recv(headerSize)

            if not len(userNameHeader):
                print("Disconnected from server")
                sys.exit()

            userNameLen = int(userNameHeader.decode("utf-8").strip())
            userName = server.recv(userNameLen).decode("utf-8")
            messageHeader = server.recv(headerSize)
            messageLen = int(messageHeader.decode("utf-8").strip())
            message = server.recv(messageLen).decode("utf-8")
            print(f"{userName}: {message}")
    except IOError as error:
        if error.errno != errno.EAGAIN and error.errno != errno.EWOULDBLOCK:
            print(f"Reading error: {str(error)}")
            sys.exit()
        continue
    except Exception as error:
        print(f"Reading error: {str(error)}")
        sys.exit()
