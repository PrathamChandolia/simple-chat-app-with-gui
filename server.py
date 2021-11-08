import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(3)

clients = []
names = []

#brodacst
def brodcast(message):
    for client in clients:
        client.send(message)

#handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{names[clients.index(client)]} says {message}")
            brodcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            names.remove(name)
            break

#receive
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))
        name = client.recv(1024)

        names.append(name)
        clients.append(client)

        print(f"Name of the client is {name}")
        brodcast(f"{name} connected to the server!\n".encode('utf-8'))
        client.send("Conneted to the server\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server running...")
recieve()
