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
    
def transformar_tamanho_imagem(caminho):
    imagem = pygame.image.load(caminho)
    imagem_redimensionada = pygame.transform.smoothscale(imagem, (LARGURA_QUADRADO, ALTURA_QUADRADO))
    imagem_redimensionada = imagem_redimensionada.convert()
    return imagem_redimensionada

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    
    i = transformar_tamanho_imagem(lista_fotos[indice_foto_atual])
    screen.blit(i, coordenada_desenhar_imagens)
    pygame.draw.rect(screen, "BLACK", quadrado, 4)
    pygame.display.flip()
    indice_foto_atual += 1
    if indice_foto_atual == 65:
        indice_foto_atual = 0

    clock.tick(30)

pygame.quit()