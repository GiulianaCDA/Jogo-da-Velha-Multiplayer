import socket
import pygame

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 8080
        self.address = (self.host, self.port)
        self.id = self.stablish_connection()
    
    def stablish_connection(self):
        self.client.connect(self.address)
        return self.client.recv(4096).decode()

    def send(self, data):
        try:
            self.client.send(data.encode('utf-8'))
            response = self.client.recv(4096).decode()
            return response
        except socket.error as error:
            return str(error)

def wait_player(rede, screen):
    arial = pygame.font.SysFont('arial', 70)
    texto = arial.render('Aguarde...', True, (255, 216, 110))
    screen.fill((18, 19, 101)) 
    screen.blit(texto, (115, 265)) 
    pygame.display.flip()
    
    player = 2
    while True:
        req = "players"
        response = rede.send(req)
        while response == '1':
            response = rede.send(req)
            player = 1
        break
    screen.fill(0) 
    return player