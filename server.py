import socket
import select
import errno
import argparse

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("-i", "--ip", required=False, help="IP Address")
argumentParser.add_argument("-p", "--port", required=False, help="Port")
args = vars(argumentParser.parse_args())

headerSize = 8

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()

if args["ip"]:
    hostIP = args["ip"]
else:
    hostIP = "0.0.0.0"

if args["port"]:
    hostPort = int(args["port"])
else:
    hostPort = 561

try:
    server.bind((hostIP, hostPort))
except socket.error as error:
    if error.errno == errno.EADDRINUSE:
        print("Port is already in use!")
    else:
        print("Binding error: " + str(error))

server.listen(5)
clientList = [server]
clients = {}

print("Machine: " + host)
print("Chat server is ready on: " + hostIP + ":" + str(hostPort))


def receive_message(client):
    try:
        receive_header = client.recv(headerSize)

        if not len(receive_header):
            return False

        message_len = int(receive_header.decode("utf-8").strip())
        return {'header': receive_header, 'data': client.recv(message_len)}
    except socket.error:
        return False


while True:
    readClients, writeClients, exceptionClients = select.select(clientList, [], clientList)

    for notifiedSocket in readClients:
        if notifiedSocket == server:
            clientSocket, clientAddress = server.accept()
            user = receive_message(clientSocket)

            if user is False:
                continue

            clientList.append(clientSocket)
            clients[clientSocket] = user
            print('New connection from {}:{}, username: {}'.format(*clientAddress, user['data'].decode('utf-8')))
        else:
            message = receive_message(notifiedSocket)

            if message is False:
                print('{} disconnected'.format(clients[notifiedSocket]['data'].decode('utf-8')))
                clientList.remove(notifiedSocket)
                del clients[notifiedSocket]
                continue

            user = clients[notifiedSocket]
            print(f'{user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for clientSocket in clients:
                if clientSocket != notifiedSocket:
                    clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notifiedSocket in exceptionClients:
        clientList.remove(notifiedSocket)
        del clients[notifiedSocket]
