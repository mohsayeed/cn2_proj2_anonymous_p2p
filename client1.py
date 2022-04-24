# Import socket module
import socket
import string	
import uuid
id = uuid.uuid4().int
port = 1024			
hostName = socket.gethostname()
hostIpAddr = socket.gethostbyname(hostName)
systemInfo = (hostIpAddr, port)
# Create a socket object
s = socket.socket()

# Define the port on which you want to connect

# connect to the server on local computer
s.connect(systemInfo)

s.send(str(id).encode())
print("Start to send the files with the client 1")
s.close()
