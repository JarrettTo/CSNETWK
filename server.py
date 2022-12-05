import socket

from _thread import *
import threading

print_lock = threading.Lock()

localIP     = "127.0.0.1"

localPort   = 20001

bufferSize  = 1024

 

msgFromServer       = "Hello UDP Client"

bytesToSend         = str.encode(msgFromServer)

 

# Create a datagram socket

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)




# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))
UDPServerSocket.listen(1)


print("UDP server up and listening")

 
connectedUsers=[]
registeredUsers=[]
# Listen for incoming datagrams
def handle_client(conn, addr):
    #bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    #message = bytesAddressPair[0]
    #address = bytesAddressPair[1]
    #   print(message.decode('ASCII'))
    while True:
        data = conn.recv(1024)
        if not data:
            print_lock.release()
            break
        try:
            print(data)
            clientMsg = eval(data.decode('ASCII'))
        except:
            print("error")
        print(clientMsg)
        if clientMsg["command"]=='join':
            if addr not in connectedUsers:
                print("WOW")
                connectedUsers.append(addr)
                print(addr)
                conn.sendto(str.encode("Connection to the Message Board Server is successful!"), addr)
            else:
                
                conn.sendto(str.encode("You're already Connected!"), addr)
        elif clientMsg["command"]=='register':
            registeredUsers.append({"handle": clientMsg['handle'], "ip": addr})
            print(registeredUsers)
            conn.sendto(str.encode("Successfully Registered!"), addr)
        elif clientMsg["command"]=='all':
            for i in connectedUsers:
                conn.sendto(str.encode(clientMsg["message"]), i)
        elif clientMsg["command"]=='message':
            for i in registeredUsers:
                if i['handle']==clientMsg['handle']:
                    conn.sendto(str.encode(clientMsg["message"]), i['ip'])
        elif clientMsg["command"]=='leave':
            for i in connectedUsers:
                if i == addr:
                    connectedUsers.remove(i)
            conn.sendto(str.encode("Connection Closed. Thank You!"), addr)

while(True):
    conn, addr = UDPServerSocket.accept()
    print_lock.acquire()
    start_new_thread(handle_client,(conn, addr))
    
   
   

    # Sending a reply to client

    