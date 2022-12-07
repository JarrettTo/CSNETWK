import socket
import threading
import queue

messages = queue.Queue()
clients = []
registeredClients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.2", 21000))

print("UDP server up and listening")


def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass
        
def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            clientMsg = eval(message.decode('ASCII'))
            print(clientMsg)
            print(addr)
            
            if clientMsg["command"]=='join':
                if addr not in clients:
                    clients.append(addr)
                    server.sendto(f"Connection to the Message Board Server is successful!".encode(), addr)
                else:
                    server.sendto(f"You're already connected!".encode(), addr)
                    
            elif clientMsg["command"]=='leave':
                for client in clients:
                    if client == addr:
                        clients.remove(client)
                for user in registeredClients:
                    if user[1] == addr:
                        registeredClients.remove(user)
                server.sendto(str.encode("Connection Closed. Thank You!"), addr)
                
            elif clientMsg["command"]=='register':
                if registeredClients:
                    flag1 = False
                    flag2 = False
                    for user in registeredClients:
                        if clientMsg["handle"].lower() == user[0].lower():
                            flag1 = True    
                        elif addr == user[1]:
                            flag2 = True
                    if flag1:
                        server.sendto(str.encode("Error: Handle or alias already exists"), addr)
                    elif flag2:
                        server.sendto(str.encode("Error: Registration failed. IP already has a Handle or Alias."), addr)
                    else:
                        registeredClients.append([clientMsg["handle"], addr])
                        server.sendto(str.encode("Welcome "+clientMsg['handle']+"!"), addr)
                    
                else:
                    registeredClients.append([clientMsg["handle"], addr])
                    server.sendto(str.encode("Welcome "+clientMsg['handle']+"!"), addr)
                    
                    
            elif clientMsg["command"]=='all':
                name="Guest"
                for user in registeredClients:
                    if user[1] == addr:
                        name=user[0]
                        
                for client in clients:
                    server.sendto(str.encode(name+": "+clientMsg["message"]), client)
                
            elif clientMsg["command"]=='msg':
                flag1 = True
                frm = "Guest"
                to = ""
                recepient = ""
                for sender in registeredClients:
                    if sender[1] == addr:
                        frm = user[0]
                for receiver in registeredClients:
                    if receiver[0] == clientMsg['handle']:
                        to = receiver[0]
                        recepient = receiver[1]
                        flag1 = False
                if flag1:
                    server.sendto(str.encode("Error: Handle or alias not found."), addr)
                else:      
                    server.sendto(str.encode("[To "+to+"]: " +clientMsg["message"]), addr)
                    server.sendto(str.encode("[From "+frm+"]: " +clientMsg["message"]), recepient)
                
                        
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

adminCommand = ""

while adminCommand != "quit":
    adminCommand = input("")
    if adminCommand == "messages":
        print (messages.qsize)
        adminCommand = ""
    elif adminCommand == "clients":
        print (clients)
        adminCommand = ""