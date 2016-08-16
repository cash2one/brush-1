import time
import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(("0.0.0.0", 3000))
serversocket.listen(1)
(clientsocket, address) = serversocket.accept()

print(str(address) + "connected")

def handler_connect(socket):
    count = 0
    while count < 7:
        time.sleep(3)
        clientsocket.send("hahah".encode())
        count = count + 1
        print("send")
    socket.close()
    
clientsocket.close()

