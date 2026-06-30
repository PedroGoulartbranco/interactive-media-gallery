from utils import caminho_recurso
import pygame
import random

class Balao(pygame.sprite.Sprite):
    def __init__(self, imagem, tamanho_tela_x, tamanho_tela_y):
        super().__init__()
        self.velocidade = random.randint(2, 7)
        self.pontos = self.velocidade * 5
        self.largura = 150
        self.altura = 150
        imagem = pygame.transform.scale(imagem, (self.largura, self.altura))

        self.image = imagem
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = random.randint(self.largura, tamanho_tela_x - self.largura)
        self.rect.y = tamanho_tela_y + (self.altura - 30)

        self.caminho = "imagens/coracao_jogo"
    def update(self):
        self.rect.y -= self.velocidade

        if self.rect.bottom < 0:
            self.kill()

class TextoPontos(pygame.sprite.Sprite):
    def __init__(self, texto, x, y, fonte):
        super().__init__()

        self.image = fonte.render(texto, True, "black")
        self.rect = self.image.get_rect(center=(x, y))
        
        self.duracao_ticks = 30
    def update(self):
        self.rect.y -= 2
        self.duracao_ticks -= 1
        
        if self.duracao_ticks <= 0:
            self.kill()