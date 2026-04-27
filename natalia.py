# Example file showing a basic pygame "game loop"
import pygame

pygame.init()
LARGURA, ALTURA = 800, 600
screen = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Te Amo Natalia")
fonte = pygame.font.SysFont('consolas', 20)

quadrado = pygame.Rect(100, 30, 600, 450)
coordenada_desenhar_imagens = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    pygame.draw.rect(screen, "BLACK", quadrado, 4)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()