import pickle
import socket
import sys
import threading
import uuid
import globals as g
import numpy as np
SIZE = 1024

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
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
clientFilesList=[]
uuid_map=[]
udp_addr_map=[]
tcp_addr_map=[]


def receiveAndSendMsg ( i,t ):
    while True:
        clients[i].send("ID".encode())
        clients[i].send(clientsid[i].encode())
        # clients[i].send("Sending uuid maps".encode())
        # if i-1>=0:
        #     clients[i].send(uuid_map[i-1].encode())
        # if i>0:
        #     clients[i-1].send("SENDING RIGHT NEIGHBOUR'S ADDRESS".encode())
        #     clients[i-1].send(tcp_addr_map[i-1])
        msg = clients[i].recv(1024)
        msg = msg.decode("utf-8")
        print(msg)


for i in range(noOfClients):
    client, addr = serverSocket.accept()
    clients.append(client)
    clientAddresses.append(addr)
    clientNames.append(client.recv(SIZE).decode("utf-8"))
    clientFilesList.append(pickle.loads(client.recv(SIZE)))
    print(clientFilesList[i])
    print("hi")
    tcp_addr_map.append(pickle.loads(client.recv(SIZE)))
    print(tcp_addr_map)
    udp_addr_map.append(client.recv(SIZE).decode())
    print(udp_addr_map)
    print("hi")

    # tcp_addr_map.append(pickle.loads(client.recv(SIZE)))
    # udp_addr_map.append(pickle.loads(client.recv(SIZE)))
    port_client = addr[1]
    id = str(uuid.uuid5(uuid.NAMESPACE_URL, str(port_client)))

    uuid_map.append(id)
    clientsid.append(id)
    clientInfo[id] = {}
    clientInfo[id]["connection"]=client
    clientInfo[id]["address"] = addr
    clientInfo[id]["active"] = True
    clientInfo[id]["files"] = clientFilesList[i]
    # g.no_of_hops = np.random.randint(size=(i+1,i+1),low=1, high=i+1, dtype=int)
    # print(g.no_of_hops)
    # print(type(tcp_addr_map[i]))


    

    threads.append(threading.Thread(target=receiveAndSendMsg,args=(i,6556)))
    threads[i].daemon = True
    threads[i].start()

for i in range(noOfClients):
	threads[i].join()