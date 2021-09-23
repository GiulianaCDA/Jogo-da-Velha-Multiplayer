import pygame
from network import Network, wait_player
from pygame.locals import MOUSEBUTTONDOWN, Rect, QUIT
from sys import exit

def desenhar_tabu():
    pygame.draw.line(tela, (255, 216, 110), (200, 40), (200, 560), 10) 
    pygame.draw.line(tela, (255, 216, 110), (400, 40), (400, 560), 10)
    pygame.draw.line(tela, (255, 216, 110), (40, 200), (560, 200), 10)
    pygame.draw.line(tela, (255, 216, 110), (40, 400), (560, 400), 10)  

def desenhar_peca(pos, quemjogou): 
    x, y = pos
    if quemjogou == 2:
        img = pygame.image.load('circle.png').convert_alpha()
        imgR = pygame.transform.scale(img, (150, 150)) 
        tela.blit(imgR, (x - 75, y - 75))
    else:
        img = pygame.image.load('x.png').convert_alpha()
        imgR = pygame.transform.scale(img, (150, 150))
        tela.blit(imgR, (x - 75, y - 75))

def testa_pos():
    for p in rec:
        if e.type == MOUSEBUTTONDOWN and p.collidepoint(mouse_pos):
            if p == rect1:
                confirmar(0, [100, 100])
            if p == rect2:
                confirmar(1, [300, 100])
            if p == rect3:
                confirmar(2, [500, 100])
            if p == rect4:
                confirmar(3, [100, 300])
            if p == rect5:
                confirmar(4, [300, 300])
            if p == rect6:
                confirmar(5, [500, 300])
            if p == rect7:
                confirmar(6, [100, 500])
            if p == rect8:
                confirmar(7, [300, 500])
            if p == rect9:
                confirmar(8, [500, 500])

def confirmar(indice, pos):
    global ESCOLHA, VEZ, espaco, rede, jogador
    if marca_tabu[indice] == 'X':
        print('X')
    elif marca_tabu[indice] == 'O':
        print('O')
    else:
        marca_tabu[indice] = ESCOLHA
        desenhar_peca(pos, jogador)
        print(marca_tabu)
        if VEZ == 1:
            VEZ = 2
        else:
            VEZ = 1
        espaco +=1
    # Avisando para o servidor que uma jogada foi feita
    rede.send(f"jogada {str(jogador)} {str(pos[0])} {str(pos[1])}")

def teste_vitoria(l):
    return ((marca_tabu[0] == l and marca_tabu[1] == l and marca_tabu[2] == l) or
        (marca_tabu[3] == l and marca_tabu[4] == l and marca_tabu[5] == l) or
        (marca_tabu[6] == l and marca_tabu[7] == l and marca_tabu[8] == l) or
        (marca_tabu[0] == l and marca_tabu[3] == l and marca_tabu[6] == l) or
        (marca_tabu[1] == l and marca_tabu[4] == l and marca_tabu[7] == l) or
        (marca_tabu[2] == l and marca_tabu[5] == l and marca_tabu[8] == l) or
        (marca_tabu[0] == l and marca_tabu[4] == l and marca_tabu[8] == l) or
        (marca_tabu[2] == l and marca_tabu[4] == l and marca_tabu[6] == l))

def texto_vitoria(v):
    opensans = pygame.font.SysFont('opensanscondensed', 45)
    mensagem = 'JOGADOR {} VENCEU'.format(v) 

    if v == 'EMPATE':
        mens_vitoria = opensans.render('DEU VELHA', True, (18, 19, 101), (255, 255, 255))
        tela.blit(mens_vitoria, (115, 265))
    else:
        mens_vitoria = opensans.render(mensagem, True, (18, 19, 101), (255, 255, 255)) 
        tela.blit(mens_vitoria, (100, 265))

def reset():
        global ESCOLHA, ESTADO, VEZ, marca_tabu, espaco
        ESTADO = 'JOGANDO'
        VEZ = 1
        ESCOLHA = 'X'
        espaco = 0
        marca_tabu = [
            0, 1, 2,
            3, 4, 5,
            6, 7, 8
        ]
        tela.fill(0)

'''def pontos(pontos1, pontos2):
    opensans = pygame.font.SysFont('opensanscondensed', 20)
    jogador1 = 'Jogador1 = {}'.format(pontos1)
    jogador2 = 'Jogador2 = {}'.format(pontos2) 

    jd1 = opensans.render(jogador1, True, (188, 186, 186))
    jd2 = opensans.render(jogador2, True, (188, 186, 186))
    tela.blit(jd1, (0, 0))
    tela.blit(jd2, (420, 0))'''

pygame.init() 

rede = Network()

tela = pygame.display.set_mode((600, 600), 0, 32)
pygame.display.set_caption('Jogo da velha') 
tela.fill((18, 19, 101)) 
# Se conectando com o servidor e aguardando os dois jogadores se conectarem
jogador = wait_player(rede, tela)
print(f'jogador: {jogador}')


ESTADO = 'JOGANDO'
VEZ = 1
ESCOLHA = 'X'
espaco = 0
marca_tabu = [
    0, 1, 2,
    3, 4, 5,
    6, 7, 8
]

rect1 = Rect((0, 0), (200, 200))
rect2 = Rect((200, 0), (200, 200))
rect3 = Rect((400, 0), (200, 200))
rect4 = Rect((0, 200), (200, 200))
rect5 = Rect((200, 200), (200, 200))
rect6 = Rect((400, 200), (200, 200))
rect7 = Rect((0, 400), (200, 200))
rect8 = Rect((200, 400), (200, 200))
rect9 = Rect((400, 400), (200, 200))

rec = [
    rect1,rect2,rect3,rect4,
    rect5,rect6,rect7,rect8,rect9,
]

pontos1, pontos2 = 0, 0

tela.fill((18, 19, 101)) 
while True:
    mouse_pos = pygame.mouse.get_pos()
    if ESTADO == 'JOGANDO':
        desenhar_tabu()
        #pontos(pontos1, pontos2)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()
            if e.type == MOUSEBUTTONDOWN:
                if VEZ == jogador:
                    if jogador == 1:
                        ESCOLHA = 'X'
                    else:
                        ESCOLHA = 'O'
                    testa_pos()

        if teste_vitoria('X'):
            rede.send("vitoria 1")
            print('X VENCEU')
            texto_vitoria('X')
            ESTADO = 'RESET'
            pontos1 += 1

        elif teste_vitoria('O'):
            rede.send("vitoria 2")
            print('O VENCEU')
            texto_vitoria('O')
            ESTADO = 'RESET'
            pontos2 +=1

        elif espaco >= 9:
            print('EMPATE')
            texto_vitoria('EMPATE')
            ESTADO = 'RESET'

    else: 
        for u in pygame.event.get():
            if u.type == QUIT:
                pygame.quit()
                exit()
            if u.type == MOUSEBUTTONDOWN:
                reset()
                desenhar_tabu()

    pygame.display.flip()
    # Buscando por updates no estado do jogo 
    response = rede.send(f"updatevez {str(VEZ)}")
    response = response.split(' ')

    if response[0] == "venceu":
        if response[1] == '1':
            texto_vitoria('X')
        else:
            texto_vitoria('O')
    if response[0] == 'u':
        VEZ = int(response[1])
        quemjogou = int(response[2])
        x = int(response[3])
        y = int(response[4])
        # Desenhado a jogada realizada pelo outro jogador
        desenhar_peca([x, y], quemjogou)