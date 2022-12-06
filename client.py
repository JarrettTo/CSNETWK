import socket



msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 20001)

bufferSize          = 1024

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(5)
 

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
                UDPClientSocket.connect((userInput.split(" ")[1], int(userInput.split(" ")[2])))
                UDPClientSocket.sendto(str.encode("{'command':'join'}"), (userInput.split(" ")[1], int(userInput.split(" ")[2])))
                port=int(userInput.split(" ")[2])
                ip=userInput.split(" ")[1]
                joinedStatus=True
                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                print(msgFromServer[0].decode('ASCII'))
            except:
                joinedStatus=False
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
            print(msgFromServer[0].decode('ASCII'))
        else:
            print("Error: Disconnection failed. Please connect to the server first.")
        
        #here
    elif userInput.split(" ")[0] == "/register" and joinedStatus==True:
        if len(userInput.split(" ")) ==2: 
            UDPClientSocket.sendto(str.encode('{"command":"register", "handle":"'+userInput.split(" ")[1]+'"}'), (ip,port))
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            print(msgFromServer[0].decode('ASCII'))
        else:
            print("Error: Command parameters do not match or is not allowed.")
    elif userInput.split(" ")[0] == "/all" and joinedStatus==True:
        if len(userInput.split(" ")) >=2: 
            UDPClientSocket.sendto(str.encode('{"command":"all", "message":"'+" ".join(userInput.split(" ")[1:])+'"}'), (ip,port))
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            print(msgFromServer[0].decode('ASCII'))
        else:
            print("Error: Command parameters do not match or is not allowed.")
    elif userInput.split(" ")[0] == "/msg" and joinedStatus==True:
        if len(userInput.split(" ")) >=3:
            UDPClientSocket.sendto(str.encode('{"command":"message", "handle":"'+userInput.split(" ")[1]+ '","message":"'+" ".join(userInput.split(" ")[2:])+'"}'), (ip,port))
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            print(msgFromServer[0].decode('ASCII'))
        else:
            print("Error: Command parameters do not match or is not allowed.")
    elif userInput.split(" ")[0] == "/?":
        print("/join <server_ip_add> <port>   Connect to the server application\n")
        print("/leave                         Disconnect from the server application\n")
        print("/register <handle>             Register a unique handle or alias\n")
        print("/all <message>                 Send message to all\n")
        print("/msg <handle> <message>        Send direct message to a single handle\n")
        print("/?                             Request command help to output all Input Syntax commands for references\n")
    elif (userInput.split(" ")[0] == "/msg" or userInput.split(" ")[0] == "/all" or userInput.split(" ")[0] == "/register") and joinedStatus==False:
        print("Error: Please connect to the server first.")
    else:
        print("Error: Command not found.")
    
    