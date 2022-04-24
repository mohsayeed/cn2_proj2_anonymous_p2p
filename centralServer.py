import sys
import socket
import threading

port = 1024
# IPv4, TCP Connection
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostName = socket.gethostname()
hostIpAddr = socket.gethostbyname(hostName)
serverInfo = (hostIpAddr, port)
serverSocket.bind(serverInfo)
serverSocket.listen()

print("Hostname of server socket : {}".format(hostName))
print("Server IP Address : {}".format(hostIpAddr))
print("Server is Up and Running...")

SIZE = 1024

cltIDs = []

"""
cltInfo
|---cltID
    |----connection
    |----address
"""
cltInfo = {}

"""
threads
|---cltID
"""
threads = {}



def receiveAndSendMsg ( cltID ):
    while True:
        print("hi")
        msg = cltInfo[cltID]["connection"].recv(SIZE).decode("utf-8")
        print("Received msg {} from client {}".format(msg, cltID))



while True:
    
    try :
        """
        Blocking Call
        
        Return value is a pair (conn, address)
        conn : new socket object usable to send and receive data on the connection
        address : address bound to the socket on the other end of the connection
        """
        cltConn, cltAddr = serverSocket.accept()
        
        # Getting Client ID
        cltID = cltConn.recv(SIZE).decode("utf-8")
        print(cltID)
        cltIDs.append(cltID)
        print(cltIDs)
        
        """
        Try to get files list from client !!!
        """
        
        # Updating Client Info
        cltInfo[cltID] = {}
        cltInfo[cltID]["connection"] = cltConn
        cltInfo[cltID]["address"] = cltAddr
        
        # Creating a thread for communication with the client
        print("line 74",cltID)
        threads[cltID] = threading.Thread(target=receiveAndSendMsg,  args=[cltID])
        threads[cltID].daemon = True
        threads[cltID].start()
        
    except KeyboardInterrupt:
        print("Server stopped..")
        cltConn.close()