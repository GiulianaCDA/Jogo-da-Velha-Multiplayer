import socket
from _thread import *

number_of_connections = 0

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_host = 'localhost'
    port = 8080
    server_adress = (server_host, port)

    try:
        #bind associa o server_socket com a porta 8080
        server_socket.bind(server_adress) 

    except socket.error as error:
        print(str(error))

    #escuta somente 2 conexões, que é o máximo de jogares existentes no jogo da velha
    server_socket.listen(2)
    print("Waiting for a connection")
    
    while True:
        conn, address = server_socket.accept()
        print("Connected to: ", address)
        global number_of_connections
        number_of_connections += 1
        start_new_thread(threaded, (conn,))

def threaded(conn):
    global number_of_connections
    conn.send(str.encode('Início'))
    VEZ = '1'
    response = ' '
    if(number_of_connections == 2):
        conn.sendall(str.encode('O jogo vai iniciar!'))
    while True:
        try:
            request = conn.recv(4096).decode('utf-8')
          #  print("Cliente disse: " + request)
            if (number_of_connections == 1):
                response = str(number_of_connections)
            elif request == 'vez atual': 
                response = VEZ
            elif request != VEZ and number_of_connections == 2:
                response = 'jogou'
                VEZ = request
                print(request)
                print(VEZ)
            else:
                response = ' '
           # print("Servidor: " + response)
            conn.sendall(str.encode(response))
        except Exception as error:
            print('Error on server side!', error)
            break

    print("Connection Closed")
    conn.close()

main()