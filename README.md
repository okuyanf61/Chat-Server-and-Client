# Chat Server and Client

Chat room written in Python with sockets.

## Usage
Before starting the client be sure that the server is running. 
#### Server
```bash
python3 server.py [-h] -i IP -p PORT
```
Ex: 
```
python3 server.py -i 0.0.0.0 -p 555
```
#### Client
```
python3 client.py [-h] -i IP -p PORT
```
Ex: 
```
python3 client.py -i 92.54.211.6 -p 36
```