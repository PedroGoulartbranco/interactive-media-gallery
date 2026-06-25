from utils import caminho_recurso
import pygame
import random

class Balao(pygame.sprite.Sprite):
    def __init__(self, imagem, tamanho_tela_x, tamanho_tela_y):
        super().__init__()
        self.velocidade = random.randint(2, 7)

        imagem = pygame.transform.scale(imagem, (150, 150))

        self.image = imagem
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = random.randint(0, tamanho_tela_x)
        self.rect.y = 600  # Começa abaixo da tela

        self.caminho = "imagens/coracao_jogo"
    def update(self):
        self.rect.y -= self.velocidade

        if self.rect.bottom < 0:
            self.kill()