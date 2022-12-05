import socket



msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 20001)

bufferSize          = 1024

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Send to server using created UDP socket



joinedStatus=False
leave=False
ip=""
port=-1
while leave!=True:
    
    userInput=input("")
    if userInput.split(" ")[0] == "/join":
        if joinedStatus==False:
            try:

                UDPClientSocket.sendto(str.encode("{'command':'join'}"), (userInput.split(" ")[1], int(userInput.split(" ")[2])))
                port=int(userInput.split(" ")[2])
                ip=userInput.split(" ")[1]
                joinedStatus=True
                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                print(msgFromServer)
            except:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        else:
            print("Error: Already Connected to A Server")   
        #here
    elif userInput.split(" ")[0] == "/leave":
        if joinedStatus==True:
            UDPClientSocket.sendto(str.encode("{'command':'leave'}"), (ip,port))    
            UDPClientSocket.close
            joinedStatus=False
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            print(msgFromServer)
        else:
            print("Error: Disconnection failed. Please connect to the server first.")
        
        #here
    elif userInput.split(" ")[0] == "/register":
        UDPClientSocket.sendto(str.encode('{"command":"register", "handle":"'+userInput.split(" ")[1]+'"}'), (ip,port))
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        print(msgFromServer)
    elif userInput.split(" ")[0] == "/all":
        UDPClientSocket.sendto(str.encode('{"command":"all", "message":"'+userInput.split(" ")[1]+'"}'), (ip,port))
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        print(msgFromServer)
    elif userInput.split(" ")[0] == "/msg":
        UDPClientSocket.sendto(str.encode('{"command":"message", "handle":"'+userInput.split(" ")[1]+ '","message":"'+userInput.split(" ")[2]+'"}'), (ip,port))
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        print(msgFromServer)
    #elif userInput.split(" ")[0] == "/?":
        
    
    