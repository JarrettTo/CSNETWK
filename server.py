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
                    server.sendto(str.encode("\tConnection to the Message Board Server is successful!"), addr)
                else:
                    server.sendto(str.encode("\tYou're already connected!"), addr)
                    
            elif clientMsg["command"]=='leave':
                for client in clients:
                    if client == addr:
                        clients.remove(client)
                for user in registeredClients:
                    if user[1] == addr:
                        registeredClients.remove(user)
                server.sendto(str.encode("\tConnection Closed. Thank You!"), addr)
                
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
                        server.sendto(str.encode("\tError: Handle or alias already exists"), addr)
                    elif flag2:
                        server.sendto(str.encode("\tError: Registration failed. IP already has a Handle or Alias."), addr)
                    else:
                        registeredClients.append([clientMsg["handle"], addr])
                        server.sendto(str.encode("Welcome "+clientMsg['handle']+"!"), addr)
                    
                else:
                    registeredClients.append([clientMsg["handle"], addr])
                    server.sendto(str.encode("Welcome "+clientMsg['handle']+"!"), addr)
                    
                    
            elif clientMsg["command"]=='all':
                flag1 = True
                name=""
                for user in registeredClients:
                    if user[1] == addr:
                        name=user[0]
                        flag1 = False
                if not flag1:
                    for client in registeredClients:
                        server.sendto(str.encode(name+": "+clientMsg["message"]), client[1])
                    print(name+": "+clientMsg["message"])
                else:
                    print("Error: You are not registered.")
                
            elif clientMsg["command"]=='msg':
                flag1 = True
                flag2 = True
                sndr = ""
                rcvr = ""
                recepient = ""
                print(clientMsg['handle'])
                for sender in registeredClients:
                    
                    if sender[1] == addr:
                        sndr = sender[0]
                        flag1 = False
                for receiver in registeredClients:
                    if receiver[0] == clientMsg['handle']:
                        rcvr = receiver[0]
                        recepient = receiver[1]
                        flag2 = False
                if flag1:
                    server.sendto(str.encode("\tError: You are not registered."), addr)
                if flag2:
                    server.sendto(str.encode("\tError: Handle or alias not found."), addr)
                else:      
                    server.sendto(str.encode("[To "+rcvr+"]: " +clientMsg["message"]), addr)
                    server.sendto(str.encode("[From "+sndr+"]: " +clientMsg["message"]), recepient)
                print("[To "+rcvr+"]: " +clientMsg["message"])
                print("[From "+sndr+"]: " +clientMsg["message"])
                
                        
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