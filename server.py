import socket;
import json

localIP     = "127.0.0.1"

localPort   = 20001

bufferSize  = 1024

 

msgFromServer       = "Hello UDP Client"

bytesToSend         = str.encode(msgFromServer)

 

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

 

print("UDP server up and listening")

 
connectedUsers=[]
registeredUsers=[]
# Listen for incoming datagrams

while(True):
    
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print(message.decode('ASCII'))
    try:
        clientMsg = eval(message.decode('ASCII'))
    except:
        print("error")
    print(clientMsg)
    if clientMsg["command"]=='join':
        if address not in connectedUsers:
            print("WOW")
            connectedUsers.append(address)
            print(address)
            UDPServerSocket.sendto(str.encode("Connection to the Message Board Server is successful!"), address)
        else:
            
            UDPServerSocket.sendto(str.encode("You're already Connected!"), address)
    elif clientMsg["command"]=='register':
        registeredUsers.append({"handle": clientMsg['handle'], "ip": address})
        print(registeredUsers)
        UDPServerSocket.sendto(str.encode("Successfully Registered!"), address)
    elif clientMsg["command"]=='all':
        for i in connectedUsers:
            UDPServerSocket.sendto(str.encode(clientMsg["message"]), i)
    elif clientMsg["command"]=='message':
        for i in registeredUsers:
            if i['handle']==clientMsg['handle']:
                UDPServerSocket.sendto(str.encode(clientMsg["message"]), i['ip'])
    elif clientMsg["command"]=='leave':
        for i in connectedUsers:
            if i == address:
                connectedUsers.remove(i)
        UDPServerSocket.sendto(str.encode("Connection Closed. Thank You!"), address)

   

    # Sending a reply to client

    