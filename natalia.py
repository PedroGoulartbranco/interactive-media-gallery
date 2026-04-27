import pygame
from utils import *

pygame.init()
LARGURA, ALTURA = 800, 600
screen = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Te Amo Natalia")
fonte = pygame.font.SysFont('consolas', 20)

LARGURA_QUADRADO, ALTURA_QUADRADO = 600, 450

quadrado = pygame.Rect(100, 30, LARGURA_QUADRADO, ALTURA_QUADRADO)
coordenada_desenhar_imagens = (100, 30)
numero_fotos, lista_fotos = listar_fotos("imagens")
indice_foto_atual = 0

seta_direita = pygame.image.load("seta.png").convert_alpha()
seta_direita = pygame.transform.scale(seta_direita, (100, 100))

seta_esquerda = pygame.image.load("seta.png").convert_alpha()
seta_esquerda = pygame.transform.scale(seta_esquerda, (100, 100))
seta_esquerda = pygame.transform.flip(seta_esquerda, True, False)

rect_seta_direita = seta_direita.get_rect(topleft=(600, 490))
rect_seta_esqurda = seta_esquerda.get_rect(topleft=(100, 490))

posicao_seta_direita = (600, 490)
posicao_seta_esqurda = (100, 490)
    
def transformar_tamanho_imagem(caminho):
    imagem = pygame.image.load(caminho)
    imagem_redimensionada = pygame.transform.smoothscale(imagem, (LARGURA_QUADRADO, ALTURA_QUADRADO))
    imagem_redimensionada = imagem_redimensionada.convert()
    return imagem_redimensionada

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if rect_seta_direita.collidepoint(mouse_pos):
                if indice_foto_atual + 1 == numero_fotos - 1:
                    indice_foto_atual = 0
                else:
                    indice_foto_atual += 1
                print(indice_foto_atual)
            if rect_seta_esqurda.collidepoint(mouse_pos):
                if indice_foto_atual - 1 == -1:
                    indice_foto_atual = numero_fotos - 1
                else:
                    indice_foto_atual -= 1
                print(indice_foto_atual)

    screen.fill("purple")
    
    i = transformar_tamanho_imagem(lista_fotos[indice_foto_atual])

    screen.blit(i, coordenada_desenhar_imagens)
    pygame.draw.rect(screen, "BLACK", quadrado, 4)
    screen.blit(seta_direita, posicao_seta_direita)
    screen.blit(seta_esquerda, posicao_seta_esqurda)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()