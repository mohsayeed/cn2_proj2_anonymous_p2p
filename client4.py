from ctypes import sizeof
import pickle
import socket
import sys
import threading
import tkinter
import globals as g
left_neigh_addr=""
right_neigh_addr=""
SIZE=1024
hostName = socket.gethostname()
client1_hostName= socket.gethostbyname(hostName)
#//////////////Connenction to CS/////////////
clientSocket_3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostIpAddr = input("Please Provide the Server IP Address : ")
clientSocket_3.connect((hostIpAddr, 1024))
print("Connected to Centralised Server")
#///////////////////////////////////////////

#///////////////Input Name //////////////////
clientName = input("Please enter your Name : ")
clientSocket_3.send(bytes(clientName,"utf-8"))
print("Transfering you to Chat Room....")
#/////////////////////////////////////////////


#/////////////send file names & recv uuid//////////////////
clientSocket_3.send(g.toBytes(g.client1_Files))
clientUUID = (clientSocket_3.recv(1024)).decode("utf-8")
print(clientUUID)
#/////////////////////////////////////////////////////////


#////////////////////////udp socket bind/////////////////
udp_client1_port = 20004
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
client1_udp_addr = (client1_hostName, udp_client1_port)
UDPServerSocket.bind(client1_udp_addr)
print("udp server is up & listening")
#/////////////////////////////////////////////////////////


clientSocket_3.send(bytes("send ip_neigh_addr","utf-8"))


#///////////////////////tcp socket bind //////////////////
# tcp_client1_port = 30001
# TCPServSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client1_tcp_addr =  (client1_hostName,tcp_client1_port)
# TCPServSocket.bind(client1_tcp_addr)
# TCPServSocket.listen()
# //////////////////////////////////////////////////////////



def receiveMsg ( msgList ):
	while True:
		message = clientSocket_3.recv(1024)
		message = message.decode("utf-8")
		if ( message.find("ACTIVE MEMBERS") != -1 ):
			msgList.insert(tkinter.END,message)
		elif ( message.find("has been added to the Chat") != -1 ):
			msgList.insert(tkinter.END,'                                {}'.format(message))
		elif(message.find("ID")!=-1):
			msgList.insert(tkinter.END,'Your Generated {}'.format(message))
		elif(message.find("RIGHT")!=-1):
			right_neigh_addr = message.split("-")[1]
			print("RIGHT         sdfkjll;dfs    ",right_neigh_addr)
		elif(message.find("LEFT")!=-1):
			left_neigh_addr = message.split("-")[1]
			print("LEFT         sdfkjll;dfs    ",left_neigh_addr)
		else:
			msgList.insert(tkinter.END,'                                                                {}'.format(message))
		



def sendMsg ( textInput, msgList, clientSocket_3 ):

	req = textInput.get()
	textInput.delete(0, tkinter.END)

	msgList.insert(tkinter.END,"You : " + req)

	if ( req.find("QUIT") != -1 ):
		clientSocket_3.send(bytes(req,"utf-8"))
		msgList.insert(tkinter.END,'You have left the chat')
		sys.exit()

	elif (req.count("FILESEND")>0):
		clientSocket_3.send(bytes(req,"utf-8"))
		x = req.split(" ")
		file = open("data/"+x[1],"rb")
		data = file.read(SIZE)
		while data:
			clientSocket_3.send(data)
			data = file.read(SIZE)
		file.close()

	else:
		clientSocket_3.send(bytes(req,"utf-8"))


chatWindow = tkinter.Tk()
chatWindow.title('Chatroom')

frameMsgs = tkinter.Frame(master=chatWindow)
scrollBar = tkinter.Scrollbar(master=frameMsgs)

msgList = tkinter.Listbox (
	master=frameMsgs, 
	yscrollcommand=scrollBar.set
)

scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=False)
msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

frameMsgs.grid(row=0, column=0, columnspan=5, sticky="nsew")

frameEntry = tkinter.Frame(master=chatWindow)
textInput = tkinter.Entry(master=frameEntry)
textInput.pack(fill=tkinter.BOTH, expand=True)

textInput.bind("<Return>", lambda x: sendMsg(textInput, msgList, clientSocket_3) )
textInput.insert(0, "Please enter your message here")

sendButton = tkinter.Button(
	master=chatWindow,
	text='send',
	command=lambda: sendMsg(textInput, msgList, clientSocket_3)
)

frameEntry.grid(row=1, column=0, padx=10, sticky="ew")
sendButton.grid(row=1, column=1, pady=10, sticky="ew")

chatWindow.rowconfigure(0, minsize=500, weight=1)
chatWindow.rowconfigure(1, minsize=50, weight=0)
chatWindow.columnconfigure(0, minsize=500, weight=1)
chatWindow.columnconfigure(1, minsize=200, weight=0)


recvThread = threading.Thread(target=receiveMsg, args=(msgList,))
recvThread.daemon = True
recvThread.start()

msgList.insert(tkinter.END,"                Welcome to the Chat Room !!")

chatWindow.mainloop()