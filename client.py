import socket



msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 20001)

bufferSize          = 1024

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

 

# Send to server using created UDP socket



joinedStatus=False
leave=False
ip=""
port=-1
while leave!=True:
    
    userInput=input("")
    if userInput.split(" ")[0] == "/join":
        if joinedStatus==False:
            UDPClientSocket.connect((userInput.split(" ")[1], int(userInput.split(" ")[2])))
            UDPClientSocket.send(str.encode("{'command':'join'}"))
            port=int(userInput.split(" ")[2])
            ip=userInput.split(" ")[1]
            
        #here
    elif userInput.split(" ")[0] == "/leave":
        UDPClientSocket.send(str.encode("{'command':'leave'}"))
        UDPClientSocket.close()    
        leave=True
        
        #here
    elif userInput.split(" ")[0] == "/register":
        UDPClientSocket.send(str.encode('{"command":"register", "handle":"'+userInput.split(" ")[1]+'"}'))
        
    elif userInput.split(" ")[0] == "/all":
        UDPClientSocket.send(str.encode('{"command":"all", "message":"'+userInput.split(" ")[1]+'"}'))
        
    elif userInput.split(" ")[0] == "/msg":
        UDPClientSocket.send(str.encode('{"command":"message", "handle":"'+userInput.split(" ")[1]+ '","message":"'+userInput.split(" ")[1]+'"}')   )
    
    msgFromServer = UDPClientSocket.recv(bufferSize)
    print(msgFromServer)
    #elif userInput.split(" ")[0] == "/?":
        #here