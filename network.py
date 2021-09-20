import socket

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
