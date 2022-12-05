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
        
        flag=False
        for i in registeredUsers:
            if i['handle']==clientMsg['handle']:
                flag=True
        if flag:
            UDPServerSocket.sendto(str.encode("Error: Registration failed. Handle or alias already exists."), address)
        else:
            registeredUsers.append({"handle": clientMsg['handle'], "ip": address})
            UDPServerSocket.sendto(str.encode("Welcome "+clientMsg['handle']+"!"), address)
        
    elif clientMsg["command"]=='all':
        
        UDPServerSocket.sendto(str.encode("[To All]: " +clientMsg["message"]), address)
        name='Guest'
        for i in registeredUsers:
            if i['ip']==address:
                name=i['handle']
        print(name+": "+ clientMsg["message"])
    elif clientMsg["command"]=='message':
        flag=False
        for i in registeredUsers:
            if i['handle']==clientMsg['handle']:
                UDPServerSocket.sendto(str.encode("[To "+i['handle']+"]: " +clientMsg["message"]), address)
                flag=True
                name='Guest'
                for j in registeredUsers:
                    if j['ip']==address:
                        name=i['handle']
                print("[From "+name+"]: "+ clientMsg["message"])
        if flag==False:
            UDPServerSocket.sendto(str.encode("Error: Handle or alias not found."), address)
        
        
    elif clientMsg["command"]=='leave':
        for i in connectedUsers:
            if i == address:
                connectedUsers.remove(i)
        UDPServerSocket.sendto(str.encode("Connection Closed. Thank You!"), address)

   

    # Sending a reply to client

    