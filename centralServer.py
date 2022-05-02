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
clientFilesList=[]



def receiveAndSendMsg ( i,t ):
    while True:
        msg = clients[i].recv(1024)
        msg = msg.decode("utf-8")
        if(msg.find("UDP_ADDR")!=-1):
            msg = msg.split("-")[1]
            clientInfo[clientsid[i]]["udp_address"] = msg
            print(msg)
        if(msg.find("send ip_neigh_addr")!=-1):
            if(i>0):
                address_left = clientInfo[clientsid[i-1]]["udp_address"]
                address_right = clientInfo[clientsid[i]]["udp_address"]
                print(address_left,"left server")
                print(address_right,"right server")
                clients[i-1].send(("RIGHT"+"-"+str(address_right)).encode())
                clients[i].send(("LEFT"+"-"+str(address_left)).encode())
        if(msg.find(g.Send_string)!=-1):
            msg_filename = msg.split(" ")[1]
            print(clientInfo)
            isFilePresentV,uuid_file = g.isFilePresent(msg_filename,clientInfo)
            if(isFilePresentV):
                print("present")
                clients[i].send(("HOP DISTANCE"+"-"+str(g.hopcount(uuid_file))).encode())
            else:
                print("not present")
                clients[i].send("NO FILE PRESENT".encode())
        
for i in range(noOfClients):
    client, addr = serverSocket.accept()
    clients.append(client)
    clientAddresses.append(addr)
    clientNames.append(client.recv(SIZE).decode("utf-8"))
    clientFilesList.append(pickle.loads(client.recv(SIZE)))
    port_client = addr[1]
    id = str(uuid.uuid5(uuid.NAMESPACE_URL, str(port_client)))
    clientsid.append(id)
    clients[i].send(clientsid[i].encode())
    clientInfo[id] = {}
    clientInfo[id]["connection"]=client
    clientInfo[id]["address"] = addr
    clientInfo[id]["active"] = True
    clientInfo[id]["files"] = clientFilesList[i]

    

    threads.append(threading.Thread(target=receiveAndSendMsg,args=(i,6556)))
    threads[i].daemon = True
    threads[i].start()

for i in range(noOfClients):
	threads[i].join()