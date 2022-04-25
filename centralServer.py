import socket
import sys
import threading
import uuid

SIZE = 1024

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostName = socket.gethostname()
host_ip_addrss= socket.gethostbyname(hostName)
print("Server IP Address : " + host_ip_addrss)
port = 1024
print("Server Connected")
serverSocket.bind((host_ip_addrss, port))

print("Hostname of server socket : " + hostName)
serverSocket.listen()

noOfClients = 3
clients = []
noOfClientsArrived = 0
clientAddresses = []
clientNames = []
threads = []
clientInfo = {}
clientsid=[]
Send_string = "FILESEND"


def receiveAndSendMsg ( i,t ):
    while True:
        
        clients[i].send(clientsid[i].encode())
        msg = clients[i].recv(1024)
        msg = msg.decode("utf-8")
        print(msg)


for i in range(noOfClients):
    client, addr = serverSocket.accept()
    clients.append(client)
    clientAddresses.append(addr)
    clientNames.append(client.recv(SIZE).decode("utf-8"))
    port_client = addr[1]
    id = str(uuid.uuid5(uuid.NAMESPACE_URL, str(port_client)))
    clientsid.append(id)
    clientInfo[id] = {}
    clientInfo[id]["connection"]=client
    clientInfo[id]["address"] = addr
    clientInfo[id]["active"] = True


    threads.append(threading.Thread(target=receiveAndSendMsg,args=(i,6556)))
    threads[i].daemon = True
    threads[i].start()

for i in range(noOfClients):
	threads[i].join()