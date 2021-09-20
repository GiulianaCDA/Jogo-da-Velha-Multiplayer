from network import Network
from time import sleep

rede = Network()

while True:
    msg = "frase em minisculo"
    response = rede.send(msg)
    print(response)
    sleep(1)