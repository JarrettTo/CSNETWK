import socket
import threading
import random
import queue

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

joined=False
leave=False
serverAddress = ("127.0.0.2", 21000)


def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass
        
t = threading.Thread(target=receive)
t.daemon = True
t.start()

while leave!= True:
    message = input("")
    command = message.split(" ")[0]
    
    if command == "/join":
        try:
            ip = message.split(" ")[1]
            port = int(message.split(" ")[2])
            try:
                if (ip == "127.0.0.2" and port == 21000):
                    client.sendto(str.encode("{'command':'join'}"), serverAddress)
                    joined = True
                else:
                    print("\tError: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            except:
                joined = False
                print("\tError: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        except:
            print("\tError: Command parameters do not match or is not allowed.")
            
    elif command == "/leave" and joined == True:
        client.sendto(str.encode("{'command':'leave'}"), serverAddress)    
        client.close
        joined = False
        
    elif command == "/register" and joined == True:
        if len(message.split(" ")) ==2:
            try:
                client.sendto(str.encode('{"command":"register", "handle":"'+message.split(" ")[1]+'"}'), serverAddress)
            except:
                print("Error: Failed to register")
        else:
            print("\tError: Command parameters do not match or is not allowed.")
        
    elif command == "/all" and joined == True:
        if len(message.split(" ")) >=2: 
            client.sendto(str.encode('{"command":"all", "message":"'+" ".join(message.split(" ")[1:])+'"}'), serverAddress)
        else:
            print("\tError: Command parameters do not match or is not allowed.")

    elif command == "/msg" and joined == True:
        if len(message.split(" ")) >=3: 
            client.sendto(str.encode('{"command":"msg", "handle":"'+message.split(" ")[1]+ '","message":"'+" ".join(message.split(" ")[2:])+'"}'), serverAddress)
        else:
            print("\tError: Command parameters do not match or is not allowed.")
        
    elif (command == "/msg" or command == "/all" or command == "/register" or command == "/leave") and joined==False:
        print("Error: Please connect to the server first.")
        
    elif command == "/?":
        print("\n\t/join <server_ip_add> <port>   Connect to the server application\n")
        print("\t/leave                         Disconnect from the server application\n")
        print("\t/register <handle>             Register a unique handle or alias\n")
        print("\t/all <message>                 Send message to all\n")
        print("\t/msg <handle> <message>        Send direct message to a single handle\n")
        print("\t/?                             Request command help to output all Input Syntax commands for references\n")
    else:
        print("Error: Command not found.")
    