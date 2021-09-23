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
    jogador = '1'
    x = '0' #inicializando x
    y = '0' #inicializando y
    ready = 0
    while True:
        try:
            request = conn.recv(4096).decode('utf-8')
            request = request.split(' ')
            op = request[0]
            print(request)
            if op == "players":
                response = str(number_of_connections)
            elif op == "jogada":
                jogador = request[1]
                x = request[2]
                y = request[3]
                if VEZ == '1':
                    VEZ = '2'
                else: VEZ = '1'
            elif op == "updatevez":
                #print(f"Vez: {VEZ} request: {request[1]}")
                if request[1] != VEZ: 
                    print(f"u {VEZ} {jogador} {x} {y}")
                    ready = 1
                    response = f"u {VEZ} {jogador} {x} {y}"
                else:
                    response = "OK"
            elif op == 'espera':
                if ready == 1: response = 'OK'
                else: response = 'esperando'
            conn.sendall(str.encode(response))
        except Exception as error:
            print('Error on server side!', error)
            break

    print("Connection Closed")
    conn.close()

main()