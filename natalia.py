from PIL import Image
import pygame

pygame.init()
LARGURA, ALTURA = 800, 600
screen = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Te Amo Natalia")
fonte = pygame.font.SysFont('consolas', 20)

teste = pygame.image.load("imagens\WhatsApp Image 2026-03-22 at 22.21.09 (2).jpeg")
imagem = teste.convert()

LARGURA_QUADRADO, ALTURA_QUADRADO = 600, 450

quadrado = pygame.Rect(100, 30, LARGURA_QUADRADO, ALTURA_QUADRADO)
coordenada_desenhar_imagens = (90, 20)

def calcular_tamanho_imagem(caminho):
    with Image.open(caminho) as img:
            return img.size
    
def transformar_tamanho_imagem(caminho):
     imagem = pygame.image.load(caminho)
     imagem_redimensionada = pygame.transform.smoothscale(imagem, (largura_ret, altura_ret))

print(calcular_tamanho_imagem("imagens/WhatsApp Image 2026-03-22 at 22.57.05.jpeg"))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    pygame.draw.rect(screen, "BLACK", quadrado, 4)
    screen.blit(imagem, coordenada_desenhar_imagens)
    pygame.display.flip()

    clock.tick(30)

pygame.quit()