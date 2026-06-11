import pygame
from utils import *
from quadrados import *
from editar_imagens import *
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops, ImageDraw
from random import choice

pygame.init()
LARGURA, ALTURA = 1000, 600
screen = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(400, 150)

caminho = None
musica_tocando = True

cores_botoes = "#6503A6"
cor_fundo_atual = "#AC01F4"
cor_borda_linhas_atual = "#000000"

largura_atual = LARGURA
altura_atual = ALTURA

i = None
angulo_atual = 0
imagem_girada = False
imagem_foi_girada_alguma_vez = False
contador_mudancas = 0

lista_imagens_pil = []

pygame.display.set_caption("Te Amo Natalia")
fonte = pygame.font.SysFont('consolas', 20)

imagem_coracao = pygame.image.load(caminho_recurso("coracao_icon.png")).convert_alpha()
imagem_coracao = pygame.transform.scale(imagem_coracao, (128, 128))
pygame.display.set_icon(imagem_coracao)

pygame.mixer.init()

tempo_para_segurar = 230 #Tempo de cooldown para um clique nao contar como dois
ultimo_click = 0

pasta_aberta = False
mostrar_botoes_laterais = True
pagina_configuracoes_aberta = False
pagina_editar_aberta = False
pagina_ler_aberta = False
pagina_supresa_aberta = False
pagina_de_ajuda = False

mudancas_nas_imagens = False
eh_para_girar = True
efeito_desenho = False
imagem_esta_desenhada = False
imagem_foi_girada = False

i_giro_atual = None

abriu_primeira_aba_vez = True

pagina_personalisar_galeria_aberta = False
pagina_inicial = True #Pagina normal

texto_botao_voltar = fonte.render("Configurações", True, "black")
texto_botao_voltar = fonte.render("Voltar", True, "black")

quadrado = pygame.Rect(DISTANCIA_LATERAL_QUADRADO, 30, LARGURA_QUADRADO, ALTURA_QUADRADO)
coordenada_desenhar_imagens = (DISTANCIA_LATERAL_QUADRADO, 30)
numero_fotos = lista_fotos = None
indice_foto_atual = 0
ponto_interrogacao = pygame.image.load(caminho_recurso("interrogacao.png")).convert_alpha()
ponto_interrogacao = pygame.transform.scale(ponto_interrogacao, (100, 100))

seta_direita = pygame.image.load(caminho_recurso("seta.png")).convert_alpha()
seta_direita = pygame.transform.scale(seta_direita, (100, 100))

seta_esquerda = pygame.image.load(caminho_recurso("seta.png")).convert_alpha()
seta_esquerda = pygame.transform.scale(seta_esquerda, (100, 100))
seta_esquerda = pygame.transform.flip(seta_esquerda, True, False)

rect_seta_direita = seta_direita.get_rect(topleft=(DISTANCIA_LATERAL_QUADRADO + 500, 490))
rect_seta_esqurda = seta_esquerda.get_rect(topleft=(DISTANCIA_LATERAL_QUADRADO, 490))
rect_ponto_interrogacao = ponto_interrogacao.get_rect(topleft=(DISTANCIA_LATERAL_QUADRADO + 250, 490))

posicao_seta_direita = (DISTANCIA_LATERAL_QUADRADO + 500, 490)
posicao_seta_esqurda = (DISTANCIA_LATERAL_QUADRADO, 490)
posicao_ponto_interrogacao = (DISTANCIA_LATERAL_QUADRADO + 250, 490)

clicou_botao_randomizar = False
fotos_opcoes = []

indice_musica = 0
nome_musica_atual, caminho_musica_atual = musica_atual(indice_musica)

pygame.mixer.music.load(caminho_musica_atual)
pygame.mixer.music.play(-1)

texto_musica_atual = texto_numero = fonte.render(nome_musica_atual, True, "black")
posicao_texto_musica = (0, 0)

texto_botao_abrir_pasta = botao_abrir_pasta = pygame.Rect(DISTANCIA_LATERAL_QUADRADO, 30, LARGURA_QUADRADO, ALTURA_QUADRADO)

botao_fundo_branco = botao_fundo_roxo = botao_fundo_cinza  = botao_fundo_azul = botao_fundo_vermelho = botao_fundo_rosa = pygame.Rect(0, 0 - 8, 40, 40)
botao_botoes_branco = botao_botoes_roxo = botao_botoes_cinza = botao_botoes_vermelho = botao_botoes_azul = botao_botoes_rosa = pygame.Rect(0, 0 - 8, 40, 40)
botao_borda_azul = botao_borda_branco = botao_borda_cinza = botao_borda_rosa = botao_borda_roxo = botao_borda_vermelho = botao_borda_preto = pygame.Rect(0, 0 - 8, 40, 40)

def transformar_tamanho_imagem(caminho):
    imagem = pygame.image.load(caminho)
    imagem_redimensionada = pygame.transform.smoothscale(imagem, (quadrado.width, quadrado.height))
    imagem_redimensionada = imagem_redimensionada.convert()
    return imagem_redimensionada

def mostrar_numero_foto_atual(indice):
    texto_numero = fonte.render(f"Foto: {indice + 1}", True, "black")
    screen.blit(texto_numero, (DISTANCIA_LATERAL_QUADRADO, 9))

def mostrar_botao_abrir_pasta():
    texto = fonte.render("Abrir Pasta", True, "black")
    coordenadas_texto = texto.get_rect(center=quadrado_cinza.center)
    pygame.draw.rect(screen, "gray", quadrado_cinza)
    screen.blit(texto, coordenadas_texto)
    return texto

def calculo_tamanho_fonte_atual(tamanho_base):
    escala = screen.get_height() / 600
    novo_tamanho = int(tamanho_base * escala)
    return pygame.font.SysFont('consolas', novo_tamanho)

def funcao_mostrar_botoes_laterais():
    texto_botao_configuracoes = fonte.render("Configurações", True, "black")
    texto_botao_editar = fonte.render("Editar", True, "black")
    texto_botao_ler = fonte.render("Leitura", True, "black")
    texto_botao_supresa = fonte.render("Mais", True, "black")

    coordenadas_texto_configuracoes = texto_botao_configuracoes.get_rect(center=botao_configuracoes.center)
    coordenadas_texto_editar = texto_botao_editar.get_rect(center=botao_editar_imagens.center)
    coordenadas_texto_ler = texto_botao_ler.get_rect(center=botao_ler.center)
    coordenadas_texto_supresa = texto_botao_supresa.get_rect(center=botao_supresa.center)

    pygame.draw.rect(screen, cores_botoes, botao_configuracoes)
    pygame.draw.rect(screen,  cores_botoes, botao_editar_imagens)
    pygame.draw.rect(screen,  cores_botoes, botao_ler)
    pygame.draw.rect(screen,  cores_botoes, botao_supresa)

    screen.blit(texto_botao_configuracoes, coordenadas_texto_configuracoes)
    screen.blit(texto_botao_editar, coordenadas_texto_editar)
    screen.blit(texto_botao_ler, coordenadas_texto_ler)
    screen.blit(texto_botao_supresa, coordenadas_texto_supresa)

#Pagina de configurações
def funcao_mostrar_pagina_configuracoes():
    texto_botao_abrir_nova_pasta = fonte.render("Abrir Pasta", True, "black")
    texto_botao_trocar_musica = fonte.render("Pular Música", True, "black")
    texto_botao_personalizar = fonte.render("Personalizar Galeria", True, "black")
    texto_botao_ajuda = fonte.render("Guia/Ajuda", True, "black")

    coordenadas_texto_voltar = texto_botao_voltar.get_rect(center=botao_voltar.center)
    coordenadas_texto_abrir_nova_pasta = texto_botao_abrir_nova_pasta.get_rect(center=botao_abrir_nova_pasta.center)
    coordenadas_texto_trocar_musica = texto_botao_trocar_musica.get_rect(center=botao_trocar_musica.center)
    coordenadas_texto_personalizar = texto_botao_personalizar.get_rect(center=botao_personalizar.center)
    coordenadas_texto_ajuda = texto_botao_ajuda.get_rect(center=botao_ajuda.center)

    pygame.draw.rect(screen, cores_botoes, botao_voltar)
    pygame.draw.rect(screen, cores_botoes, botao_abrir_nova_pasta)
    pygame.draw.rect(screen, cores_botoes, botao_trocar_musica)
    pygame.draw.rect(screen, cores_botoes, botao_personalizar)
    pygame.draw.rect(screen, cores_botoes, botao_ajuda)

    screen.blit(texto_botao_voltar, coordenadas_texto_voltar)
    screen.blit(texto_botao_abrir_nova_pasta, coordenadas_texto_abrir_nova_pasta)
    screen.blit(texto_botao_trocar_musica, coordenadas_texto_trocar_musica)
    screen.blit(texto_botao_personalizar, coordenadas_texto_personalizar)
    screen.blit(texto_botao_ajuda, coordenadas_texto_ajuda)

def atualizar_tamanho(largura, altura):
    escala_x = largura / LARGURA
    escala_y = altura / ALTURA

    nova_largura = 300 * escala_x
    nova_altura = 80 * escala_y

    nova_largura_botoes_menores = botao_girar_foto.width * escala_x
    nova_altura_botoes_menores = botao_girar_foto.height * escala_y

    x_pos = (600 * escala_x) + (70 * escala_x)
    x_pos_botoes_menores = (300 * escala_x) + (70 * escala_x)

    botao_configuracoes.width = nova_largura
    botao_configuracoes.height = nova_altura
    botao_configuracoes.x = x_pos
    botao_configuracoes.y = 30 * escala_y

    botao_editar_imagens.width = nova_largura
    botao_editar_imagens.height = nova_altura
    botao_editar_imagens.x = x_pos
    botao_editar_imagens.y = (60 + 80) * escala_y

    botao_ler.width = nova_largura
    botao_ler.height = nova_altura
    botao_ler.x = x_pos
    botao_ler.y = (160 + 80) * escala_y

    botao_supresa.width = nova_largura
    botao_supresa.height = nova_altura
    botao_supresa.x = x_pos
    botao_supresa.y = (260 + 80) * escala_y

    #Botoes de configurações
    botao_abrir_nova_pasta.width = nova_largura
    botao_abrir_nova_pasta.height = nova_altura
    botao_abrir_nova_pasta.x = x_pos
    botao_abrir_nova_pasta.y = 30 * escala_y

    botao_voltar.width = nova_largura
    botao_voltar.height = nova_altura
    botao_voltar.x = x_pos
    botao_voltar.y = (360 + 80) * escala_y

    botao_trocar_musica.width = nova_largura
    botao_trocar_musica.height = nova_altura
    botao_trocar_musica.x = x_pos
    botao_trocar_musica.y = (60 + 80) * escala_y

    botao_personalizar.width = nova_largura
    botao_personalizar.height = nova_altura
    botao_personalizar.x = x_pos
    botao_personalizar.y = (160 + 80) * escala_y

    botao_ajuda.width = nova_largura
    botao_ajuda.height = nova_altura
    botao_ajuda.x = x_pos
    botao_ajuda.y = (260 + 80) * escala_y

    botao_girar_foto.width = nova_largura_botoes_menores
    botao_girar_foto.height = nova_altura_botoes_menores
    botao_girar_foto.x = x_pos
    botao_girar_foto.y = 30 * escala_y

    botao_cores_foto.width = nova_largura_botoes_menores
    botao_cores_foto.height = nova_altura_botoes_menores
    botao_cores_foto.x = x_pos + botao_girar_foto.width + 20
    botao_cores_foto.y = 30 * escala_y

    botao_desenho_foto.width = nova_largura_botoes_menores
    botao_desenho_foto.height = nova_altura_botoes_menores
    botao_desenho_foto.x = x_pos
    botao_desenho_foto.y = 130 * escala_y

    botao_desfoque_foto.width = nova_largura_botoes_menores
    botao_desfoque_foto.height = nova_altura_botoes_menores
    botao_desfoque_foto.x = x_pos + botao_desenho_foto.width + 20
    botao_desfoque_foto.y = 130 * escala_y

    botao_vinheta_foto.width = nova_largura_botoes_menores
    botao_vinheta_foto.height = nova_altura_botoes_menores
    botao_vinheta_foto.x = x_pos
    botao_vinheta_foto.y = botao_desfoque_foto.y + 100 * escala_y

    botao_espelhar_foto.width = nova_largura_botoes_menores
    botao_espelhar_foto.height = nova_altura_botoes_menores
    botao_espelhar_foto.x = x_pos + botao_desenho_foto.width + 20
    botao_espelhar_foto.y = botao_desfoque_foto.y + 100 * escala_y

    botao_aleatorizar_foto.width = nova_largura_botoes_menores
    botao_aleatorizar_foto.height = nova_altura_botoes_menores
    botao_aleatorizar_foto.x = x_pos
    botao_aleatorizar_foto.y = botao_vinheta_foto.y + 100 * escala_y

    botao_resetar_foto.width = nova_largura_botoes_menores
    botao_resetar_foto.height = nova_altura_botoes_menores
    botao_resetar_foto.x = x_pos + botao_aleatorizar_foto.width + 20
    botao_resetar_foto.y = botao_vinheta_foto.y + 100 * escala_y

    botao_voltar_editar.width = (botao_vinheta_foto.width + 20 + botao_espelhar_foto.width)
    botao_voltar_editar.height = nova_altura
    botao_voltar_editar.x = x_pos
    botao_voltar_editar.y = botao_aleatorizar_foto.y + 100 * escala_y

def atualizar_tamanho_quadrado(largura, altura):
    global coordenada_desenhar_imagens, DISTANCIA_LATERAL_QUADRADO
    escala_x = largura / LARGURA
    escala_y = altura / ALTURA

    quadrado.width = LARGURA_QUADRADO * escala_x
    quadrado.height = ALTURA_QUADRADO * escala_y

    quadrado_cinza.width =  LARGURA_QUADRADO * escala_x
    quadrado_cinza.height = ALTURA_QUADRADO * escala_y

    quadrado.x = DISTANCIA_LATERAL_QUADRADO * escala_x
    quadrado.y = 30 * escala_y

    quadrado_cinza.x = DISTANCIA_LATERAL_QUADRADO * escala_x
    quadrado_cinza.y = 30 * escala_y

    DISTANCIA_LATERAL_QUADRADO = DISTANCIA_LATERAL_QUADRADO * escala_x

    coordenada_desenhar_imagens = (quadrado_cinza.x, quadrado_cinza.y)

def atualizar_botoes_de_imagem(largura, altura):
    global seta_esquerda, posicao_seta_esqurda, rect_seta_esqurda, seta_direita, rect_seta_direita, posicao_seta_direita, ponto_interrogacao, rect_ponto_interrogacao, posicao_ponto_interrogacao
    escala_x = largura / LARGURA
    escala_y = altura / ALTURA

    nova_largura = 100 * escala_x
    nova_altura = 100 * escala_y

    seta_esquerda = pygame.transform.scale(seta_esquerda, (int(nova_largura), int(nova_altura)))
    seta_direita = pygame.transform.scale(seta_direita, (int(nova_largura), int(nova_altura)))
    ponto_interrogacao = pygame.transform.scale(ponto_interrogacao, (int(nova_largura), int(nova_altura)))

    rect_seta_esqurda.x = DISTANCIA_LATERAL_QUADRADO * escala_x
    rect_seta_esqurda.y = 490 * escala_y
    posicao_seta_esqurda = (rect_seta_esqurda.x, rect_seta_esqurda.y)
    
    rect_seta_direita.x = (DISTANCIA_LATERAL_QUADRADO +500) * escala_x
    rect_seta_direita.y = 490 * escala_y
    posicao_seta_direita = (rect_seta_direita.x, rect_seta_direita.y)

    rect_ponto_interrogacao.x = (DISTANCIA_LATERAL_QUADRADO + 250) * escala_x
    rect_ponto_interrogacao.y = 490 * escala_y
    posicao_ponto_interrogacao = (rect_ponto_interrogacao.x, rect_ponto_interrogacao.y)


def funcao_pagina_personalisar():
    global botao_fundo_azul, botao_fundo_branco, botao_fundo_vermelho, botao_fundo_cinza, botao_fundo_roxo, botao_fundo_rosa
    global botao_botoes_azul, botao_botoes_branco, botao_botoes_cinza, botao_botoes_roxo, botao_botoes_vermelho, botao_botoes_rosa
    global botao_borda_azul, botao_borda_branco, botao_borda_cinza, botao_borda_rosa, botao_borda_roxo, botao_botoes_vermelho, botao_borda_preto
    DISTANCIA_TEXTO_PERSONALIZAR = 25

    fonte_atual = calculo_tamanho_fonte_atual(30)
    texto_titulo = fonte_atual.render("Personalizar Galeria", True, "black")
    texto_personalizar_fundo = fonte_atual.render("Cor Fundo: ", True, "black")
    texto_personalizar_botoes = fonte_atual.render("Cor Botões:", True, "black")
    texto_personalizar_borda = fonte_atual.render("Cor Bordas: ", True, "black")

    coordenadas_titulo_texto = texto_titulo.get_rect()
    coordenadas_titulo_texto.centerx = largura_atual / 2
    coordenadas_titulo_texto.top = 30

    DISTANCIA_DO_TITULO = coordenadas_titulo_texto.top + 67

    coordenadas_texto_personalizar_fundo = texto_personalizar_fundo.get_rect()
    coordenadas_texto_personalizar_fundo.top = DISTANCIA_DO_TITULO
    coordenadas_texto_personalizar_fundo.left = DISTANCIA_TEXTO_PERSONALIZAR

    coordenadas_texto_personalizar_botoes = texto_personalizar_botoes.get_rect()
    coordenadas_texto_personalizar_botoes.top = DISTANCIA_DO_TITULO + 80
    coordenadas_texto_personalizar_botoes.left = DISTANCIA_TEXTO_PERSONALIZAR

    coordenadas_texto_personalizar_bordas = texto_personalizar_borda.get_rect()
    coordenadas_texto_personalizar_bordas.top = DISTANCIA_DO_TITULO + 160
    coordenadas_texto_personalizar_bordas.left = DISTANCIA_TEXTO_PERSONALIZAR

    DISTANCIA_PAREDE_BOTOES_COR = coordenadas_texto_personalizar_botoes.right + 60
    #Fundo
    botao_fundo_branco = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR, coordenadas_texto_personalizar_fundo.y - 8, 40, 40)
    botao_fundo_roxo = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 80, coordenadas_texto_personalizar_fundo.y - 8, 40, 40)
    botao_fundo_cinza = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 160, coordenadas_texto_personalizar_fundo.y - 8, 40, 40)
    botao_fundo_azul = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 240, coordenadas_texto_personalizar_fundo.y - 8, 40, 40)
    botao_fundo_vermelho = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 320, coordenadas_texto_personalizar_fundo.y - 8, 40, 40)
    botao_fundo_rosa = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 400, coordenadas_texto_personalizar_fundo.y - 8, 40, 40)

    #Botoes
    botao_botoes_branco = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR, coordenadas_texto_personalizar_botoes.y - 8, 40, 40)
    botao_botoes_roxo = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 80, coordenadas_texto_personalizar_botoes.y - 8, 40, 40)
    botao_botoes_cinza = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 160, coordenadas_texto_personalizar_botoes.y - 8, 40, 40)
    botao_botoes_azul = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 240, coordenadas_texto_personalizar_botoes.y - 8, 40, 40)
    botao_botoes_vermelho = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 320, coordenadas_texto_personalizar_botoes.y - 8, 40, 40)
    botao_botoes_rosa = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 400, coordenadas_texto_personalizar_botoes.y - 8, 40, 40)

    #Bordas
    botao_borda_branco = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR, coordenadas_texto_personalizar_bordas.y - 8, 40, 40)
    botao_borda_roxo = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 80, coordenadas_texto_personalizar_bordas.y - 8, 40, 40)
    botao_borda_cinza = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 160, coordenadas_texto_personalizar_bordas.y - 8, 40, 40)
    botao_borda_azul = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 240, coordenadas_texto_personalizar_bordas.y - 8, 40, 40)
    botao_borda_vermelho = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 320, coordenadas_texto_personalizar_bordas.y - 8, 40, 40)
    botao_borda_rosa = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 400, coordenadas_texto_personalizar_bordas.y - 8, 40, 40)
    botao_borda_preto = pygame.Rect(DISTANCIA_PAREDE_BOTOES_COR + 480, coordenadas_texto_personalizar_bordas.y - 8, 40, 40)

    dicionario_cor_fundo = {
        "#FFFFFF": botao_fundo_branco,
        "#AC01F4": botao_fundo_roxo,
        "#6B7074": botao_fundo_cinza,
        "#FD0E0E": botao_fundo_vermelho,
        "#1F8BE4": botao_fundo_azul,
        "#F4C2C2": botao_fundo_rosa
    }

    dicionario_cor_botao = {
        "#FFFFFF": botao_botoes_branco,
        "#6503A6": botao_botoes_roxo,
        "#6B7074": botao_botoes_cinza,
        "#FD0E0E": botao_botoes_vermelho,
        "#1F8BE4": botao_botoes_azul,
        "#F4C2C2": botao_botoes_rosa
    }

    dicionario_cor_borda = {
        "#FFFFFF": botao_borda_branco,
        "#6503A6": botao_borda_roxo,
        "#6B7074": botao_borda_cinza,
        "#FD0E0E": botao_borda_vermelho,
        "#1F8BE4": botao_borda_azul,
        "#F4C2C2": botao_borda_rosa,
        "#000000": botao_borda_preto
    }

    screen.blit(texto_titulo, coordenadas_titulo_texto)
    pygame.draw.line(screen, cor_borda_linhas_atual, (0, coordenadas_titulo_texto.bottom + 3), (largura_atual, coordenadas_titulo_texto.bottom + 3), 1)
    screen.blit(texto_personalizar_fundo, coordenadas_texto_personalizar_fundo)
    pygame.draw.line(screen, cor_borda_linhas_atual, (0, coordenadas_texto_personalizar_fundo.bottom + 10), (largura_atual, coordenadas_texto_personalizar_fundo.bottom + 10), 1)
    screen.blit(texto_personalizar_botoes, coordenadas_texto_personalizar_botoes)
    pygame.draw.line(screen, cor_borda_linhas_atual, (0, coordenadas_texto_personalizar_botoes.bottom + 10), (largura_atual, coordenadas_texto_personalizar_botoes.bottom + 10), 1)
    screen.blit(texto_personalizar_borda, coordenadas_texto_personalizar_bordas)

    for botao in dicionario_cor_fundo:
        if cor_fundo_atual == botao:
            pygame.draw.rect(screen, "black", dicionario_cor_fundo[botao], 2)
        else:
            pygame.draw.rect(screen, botao, dicionario_cor_fundo[botao])

    for botao in dicionario_cor_botao:
        if cores_botoes == botao:
            pygame.draw.rect(screen, "black", dicionario_cor_botao[botao], 2)
        elif botao == cor_fundo_atual:
            pygame.draw.rect(screen, "#3bee2b", dicionario_cor_botao[botao], 2)
        else:
            pygame.draw.rect(screen, botao, dicionario_cor_botao[botao])

    for botao in dicionario_cor_borda:
        if cor_borda_linhas_atual == botao and botao != botao_borda_preto:
            pygame.draw.rect(screen, "black", dicionario_cor_borda[botao], 2)
        elif botao == cor_fundo_atual:
            pygame.draw.rect(screen, "#3bee2b", dicionario_cor_borda[botao], 2)
        else:
            pygame.draw.rect(screen, botao, dicionario_cor_borda[botao])

    coordenadas_texto_voltar = texto_botao_voltar.get_rect(center=botao_voltar.center)
    pygame.draw.rect(screen, cores_botoes, botao_voltar)
    screen.blit(texto_botao_voltar, coordenadas_texto_voltar)

def funcao_mostrar_pagina_ajuda():
    fonte_atual = calculo_tamanho_fonte_atual(30)
    fonte_texto = calculo_tamanho_fonte_atual(25)
    texto_titulo = fonte_atual.render("Guia/Ajuda", True, "black")

    texto = """<  ===> Ir para a imagem da esquerda, você pode segurar esse botão\n> ===> Ir para a imagem da direita, você pode segurar esse botão\n1 ===> Ir para primeira imagem\n2 ===> Ir para ultima imagem\nSpace ===> Escolher uma foto aleatoria\nA ===> Embaralhar as fotos\nS ===> Desembaralhar as fotos\n↑ ===> Trocar de música\n↓ ===> Trocar de música\nL ===> Abrir página de ajuda\nR ===> Resetar Imagem (Deixar ela original)
    """

    linhas = texto.split('\n')

    coordenadas_titulo_texto = texto_titulo.get_rect()
    coordenadas_titulo_texto.centerx = largura_atual / 2
    coordenadas_titulo_texto.top = 15

    DISTANCIA_TEXTO_DO_TITULO = coordenadas_titulo_texto.bottom + 40

    for i, linha in enumerate(linhas):
        tranformar_texto = fonte.render(linha, True, "black")
        pos_y = DISTANCIA_TEXTO_DO_TITULO + (i * 40)
        screen.blit(tranformar_texto, (30, pos_y))

    screen.blit(texto_titulo, coordenadas_titulo_texto)
    pygame.draw.line(screen, cor_borda_linhas_atual, (0, coordenadas_titulo_texto.bottom + 3), (largura_atual, coordenadas_titulo_texto.bottom + 3), 1)

    coordenadas_texto_voltar = texto_botao_voltar.get_rect(center=botao_voltar.center)
    pygame.draw.rect(screen, cores_botoes, botao_voltar)
    screen.blit(texto_botao_voltar, coordenadas_texto_voltar)

def funcao_mostrar_pagina_editar_imagens():
    fonte_atual = calculo_tamanho_fonte_atual(20)
    texto_girar_foto = fonte_atual.render("Girar Foto", True, "black")
    texto_botao_cores = fonte_atual.render("Cores", True, "black")
    texto_botao_desenho = fonte_atual.render("Desenho", True, "black")
    texto_botao_desfoque = fonte_atual.render("Desfoque", True, "black")
    texto_botao_vinheta = fonte_atual.render("Vinheta", True, "black")
    texto_botao_espelhar = fonte_atual.render("Espelhar", True, "black")
    texto_botao_aleatorizar = fonte_atual.render("Aleatorizar", True, "black")
    texto_botao_resetar = fonte_atual.render("Resetar", True, "black")
    texto_botao_voltar = fonte_atual.render("Voltar", True, "black")

    coordenadas_texto_girar_foto = texto_girar_foto.get_rect(center=botao_girar_foto.center)
    coordenadas_texto_botao_cores = texto_botao_cores.get_rect(center=botao_cores_foto.center)
    coordenadas_texto_botao_desenho = texto_botao_desenho.get_rect(center=botao_desenho_foto.center)
    coordenadas_texto_botao_desfoque = texto_botao_desfoque.get_rect(center=botao_desfoque_foto.center)
    coordenadas_texto_botao_vinheta = texto_botao_vinheta.get_rect(center=botao_vinheta_foto.center)
    coordenadas_texto_botao_espelhar = texto_botao_espelhar.get_rect(center=botao_espelhar_foto.center)
    coordenadas_texto_botao_aleatorizar = texto_botao_aleatorizar.get_rect(center=botao_aleatorizar_foto.center)
    coordenadas_texto_botao_resetar = texto_botao_resetar.get_rect(center=botao_resetar_foto.center)
    coordenadas_texto_botao_voltar = texto_botao_voltar.get_rect(center=botao_voltar_editar.center)

    for botao in lista_botoes_editar:
        pygame.draw.rect(screen, cores_botoes, botao)

    screen.blit(texto_girar_foto, coordenadas_texto_girar_foto)
    screen.blit(texto_botao_cores, coordenadas_texto_botao_cores)
    screen.blit(texto_botao_desenho, coordenadas_texto_botao_desenho)
    screen.blit(texto_botao_desfoque, coordenadas_texto_botao_desfoque)
    screen.blit(texto_botao_vinheta, coordenadas_texto_botao_vinheta)
    screen.blit(texto_botao_espelhar, coordenadas_texto_botao_espelhar)
    screen.blit(texto_botao_aleatorizar, coordenadas_texto_botao_aleatorizar)
    screen.blit(texto_botao_resetar, coordenadas_texto_botao_resetar)
    screen.blit(texto_botao_voltar, coordenadas_texto_botao_voltar)

def funcao_efeito_desenho(surface_pygame):
    modo = "RGBA" if surface_pygame.get_alpha() else "RGB"

    imagem_bytes = pygame.image.tobytes(surface_pygame, modo)
    imagem_pil = Image.frombytes(modo, surface_pygame.get_size(), imagem_bytes)
    
    imagem_cinza = imagem_pil.convert("L")
    
    bordas = imagem_cinza.filter(ImageFilter.FIND_EDGES)
    traços_do_lapis = ImageOps.invert(bordas)
    
    imagem_desenho = Image.blend(imagem_cinza, traços_do_lapis, alpha=0.6)

    imagem_desenho = ImageEnhance.Contrast(imagem_desenho).enhance(1.5) 
    imagem_desenho = ImageEnhance.Brightness(imagem_desenho).enhance(1.2) 
    
    imagem_desenho = imagem_desenho.convert(modo)
    surface_desenho = pygame.image.frombytes(imagem_desenho.tobytes(), imagem_desenho.size, modo)
    
    return surface_desenho

imagem_girada = False
imagem_desenha = False
imagem_mudaca = False
imagem_desfoque = False
imagem_vinheta = False
imagem_espelhada = False
imagem_raioX = False
posicao_giro = 0

def pygame_para_pillow(surface):
    modo = "RGBA" if surface.get_alpha() else "RGB"

    dados = pygame.image.tobytes(surface, modo)

    imagem_pil = Image.frombytes(
        modo,
        surface.get_size(),
        dados
    )

    return imagem_pil

vinheta_mask = Image.new("L", (quadrado.width, quadrado.height), 0)
draw = ImageDraw.Draw(vinheta_mask)
ultimo_tamanho_vinheta = None

def criar_vinheta():
    global vinheta_mask, ultimo_tamanho_vinheta

    largura = quadrado.width
    altura = quadrado.height

    ultimo_tamanho_vinheta = (largura, altura)

    vinheta_mask = Image.new("L", (largura, altura), 0)

    draw = ImageDraw.Draw(vinheta_mask)

    maior = max(largura, altura)

    for i in range(maior, 0, -5):

        cor = int(255 * (1 - (i / maior)))

        draw.ellipse(
            (
                largura/2-i,
                altura/2-i,
                largura/2+i,
                altura/2+i
            ),
            fill=cor
        )

    # vinheta_mask = ImageOps.invert(vinheta_mask)

    vinheta_mask = vinheta_mask.convert("RGB")

criar_vinheta()

def aplicar_efeitos(imagem_pillow):
    global posicao_giro, imagem_desenha, quadrado
   
    img_temp = imagem_pillow.copy()
   
    if posicao_giro == 3:
        img_temp = img_temp.transpose(Image.ROTATE_90)   # Direita
    elif posicao_giro == 2:
        img_temp = img_temp.transpose(Image.ROTATE_180)  # De ponta-cabeça (Cima)
    elif posicao_giro == 1:
        img_temp = img_temp.transpose(Image.ROTATE_270)  # Esquerda

    img_temp = img_temp.resize((quadrado.width, quadrado.height))

    if imagem_espelhada:
        img_temp = img_temp.transpose(Image.FLIP_LEFT_RIGHT)
   
    if imagem_desenha:
        img_temp = img_temp.convert("L") 
        
        img_temp = img_temp.filter(ImageFilter.FIND_EDGES)
        
        img_temp = ImageOps.invert(img_temp)
        
        img_temp = img_temp.convert("RGB")


    if imagem_vinheta:
        if ultimo_tamanho_vinheta != (quadrado.width,quadrado.height):
            criar_vinheta()

        img_temp = ImageChops.multiply(
            img_temp,
            vinheta_mask
        )

    if imagem_desfoque:
        img_temp = img_temp.filter(ImageFilter.GaussianBlur(radius=5))

    if imagem_raioX:
        # Primeiro, garante que está em RGB e inverte as cores (negativo)
        img_temp = img_temp.convert("RGB")
        img_temp = ImageOps.invert(img_temp)
       
        # Matriz que destaca o Azul/Ciano e remove o Vermelho
        matriz_raiox = (
            0.0, 0.0, 0.0, 0,    # Remove totalmente o Vermelho (R)
            0.0, 0.5, 0.3, 0,    # Deixa o Verde (G) mais suave
            0.0, 0.4, 1.0, 0     # Dá foco total no Azul (B)
        )
        img_temp = img_temp.convert("RGB", matriz_raiox)


    # if imagem_preto is not False:
    #     img_temp = img_temp.convert("RGB", imagem_preto)
    # if imagem_sepia is not False:
    #     img_temp = img_temp.convert("RGB", imagem_sepia)
    # if imagem_vermelho is not False:
    #     img_temp = img_temp.convert("RGB", imagem_vermelho)


    modo = img_temp.mode
    tamanho = img_temp.size
    dados = img_temp.tobytes()
   
    return pygame.image.fromstring(dados, tamanho, modo)

def resetar_imagem():
    global imagem_raioX, imagem_desenha, imagem_espelhada, posicao_giro, imagem_desfoque, imagem_vinheta

    imagem_vinheta = imagem_raioX = imagem_desenha = imagem_espelhada =imagem_desfoque = False
    posicao_giro = 0

def aleatorizar_efeitos():
    global imagem_raioX, imagem_desenha, imagem_espelhada, posicao_giro, imagem_desfoque, imagem_vinheta
    lista_numeros_aleatorios = []
    numero_efeitos = 4
    resetar_imagem()
    for i in range(numero_efeitos):
        lista_numeros_aleatorios.append(choice([True, False]))
    
    posicao_giro = choice([1, 2, 3, 0])
    
    for indice, i in enumerate(lista_numeros_aleatorios):
        if indice == 0:
            imagem_desenha = i
        elif indice == 1:
            imagem_espelhada = i
        elif indice == 2:
            imagem_desfoque = i
        elif indice == 3:
            imagem_vinheta = i

def funcao_mostrar_pagina_ler():
    fonte_atual = calculo_tamanho_fonte_atual(30)
    fonte_texto = calculo_tamanho_fonte_atual(20)
    texto_titulo = fonte_atual.render("EU TE AMO MUITO", True, "black")

    texto = """  Não existem palavras para descrever o quanto eu te amo do fundo do meu coração, \no quanto eu gosto de passar meu tempo com você, de ouvir sua risada, de conversar\ncom você, jogar com você entre infinitas outras coisas. Eu quero que continuemos\njuntos para todo sempre, porque além de ser minha namorada você é minha melhor amiga,\nminha parceira, minha tudo.\n Espero que você goste dessa galeria que eu fiz para nós, minha maior diversão \nfazendo for ver nossas fotos e perceber o quanto fomos ficando mais próximos e mais\na vontade um com o outro.\nASS: Com Amor Pedro!"""

    linhas = texto.split('\n')

    coordenadas_titulo_texto = texto_titulo.get_rect()
    coordenadas_titulo_texto.centerx = largura_atual / 2
    coordenadas_titulo_texto.top = 15

    DISTANCIA_TEXTO_DO_TITULO = coordenadas_titulo_texto.bottom + 40

    screen.blit(texto_titulo, coordenadas_titulo_texto)
    pygame.draw.line(screen, cor_borda_linhas_atual, (0, coordenadas_titulo_texto.bottom + 3), (largura_atual, coordenadas_titulo_texto.bottom + 3), 1)

    for i, linha in enumerate(linhas):
        tranformar_texto = fonte_texto.render(linha, True, "black")
        pos_y = DISTANCIA_TEXTO_DO_TITULO + (i * 40)
        screen.blit(tranformar_texto, (30, pos_y))

    coordenadas_texto_voltar = texto_botao_voltar.get_rect(center=botao_voltar.center)
    pygame.draw.rect(screen, cores_botoes, botao_voltar)
    screen.blit(texto_botao_voltar, coordenadas_texto_voltar)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            atualizar_tamanho(event.w, event.h)
            atualizar_tamanho_quadrado(event.w, event.h)
            atualizar_botoes_de_imagem(event.w, event.h)
            largura_atual = event.w
            altura_atual = event.h
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if pagina_inicial:
                if rect_seta_direita.collidepoint(mouse_pos):
                    if pasta_aberta:
                        if indice_foto_atual== numero_fotos - 1:
                            indice_foto_atual = 0
                        else:
                            indice_foto_atual += 1
                if rect_seta_esqurda.collidepoint(mouse_pos):
                    if pasta_aberta:
                        if indice_foto_atual - 1 == -1:
                            indice_foto_atual = numero_fotos - 1
                        else:
                            indice_foto_atual -= 1
                if rect_ponto_interrogacao.collidepoint(mouse_pos):
                    if pasta_aberta:
                        aleatorizar(numero_fotos, indice_foto_atual)
                        ticks_clicou_randozimar = pygame.time.get_ticks()
                        clicou_botao_randomizar = True
                if quadrado_cinza.collidepoint(mouse_pos):
                    if pasta_aberta is False:
                        caminho = abrir_pasta()
                        if verificar_pasta(caminho):
                            pasta_aberta = True
                            numero_fotos, lista_fotos = listar_fotos(caminho)
                            # lista_imagens_pil = []
                            # lista_imagens_pil = tranformar_imagens_para_pilow_lista(lista_fotos, lista_imagens_pil)
                            if numero_fotos == 0:
                                pasta_aberta = False
            if mostrar_botoes_laterais:
                if botao_configuracoes.collidepoint(mouse_pos):
                    mostrar_botoes_laterais = False
                    pagina_configuracoes_aberta = True
                if botao_editar_imagens.collidepoint(mouse_pos):
                    pagina_editar_aberta = True
                    tempo_quando_abriu_editar = ticks_atuais
                    mostrar_botoes_laterais = False
                if botao_ler.collidepoint(mouse_pos):
                    mostrar_botoes_laterais = False
                    pagina_inicial = False
                    pagina_ler_aberta = True
                if botao_supresa.collidepoint(mouse_pos):
                    pass
                    #mostrar_botoes_laterais = False
            #Se a pagina de configurações estiver aberta
            if pagina_configuracoes_aberta:
                if abriu_primeira_aba_vez is False:
                    abriu_primeira_aba_vez = True
                else:
                    abriu_primeira_aba_vez = False
                if botao_voltar.collidepoint(mouse_pos):
                    pagina_configuracoes_aberta = False
                    mostrar_botoes_laterais = True
                if botao_trocar_musica.collidepoint(mouse_pos):
                    if indice_musica == 0:
                        indice_musica = 1
                    else:
                        indice_musica = 0
                    nome_musica_atual, caminho_musica_atual = tocar_musica(indice_musica)
                    pygame.mixer.music.load(caminho_musica_atual)
                    pygame.mixer.music.play(-1)
                if botao_abrir_nova_pasta.collidepoint(mouse_pos) and abriu_primeira_aba_vez  is False:
                    caminho_novo = abrir_pasta()
                    if verificar_pasta(caminho_novo):
                        pasta_aberta = True
                        caminho = caminho_novo
                        numero_fotos, lista_fotos = listar_fotos(caminho)
                        if numero_fotos == 0:
                            pasta_aberta = False
                if botao_personalizar.collidepoint(mouse_pos):
                    pagina_inicial = False
                    pagina_personalisar_galeria_aberta = True
                    pagina_configuracoes_aberta = False
                if botao_ajuda.collidepoint(mouse_pos):
                    pagina_inicial = False
                    pagina_configuracoes_aberta = False
                    pagina_de_ajuda = True
            if pagina_personalisar_galeria_aberta:
                if botao_voltar.collidepoint(mouse_pos):
                    pagina_configuracoes_aberta = True
                    pagina_inicial = True
                    pagina_personalisar_galeria_aberta = False
                if botao_fundo_branco.collidepoint(mouse_pos):
                    cor_fundo_atual = "#FFFFFF"
                if botao_fundo_roxo.collidepoint(mouse_pos):
                    cor_fundo_atual = "#AC01F4"
                if botao_fundo_vermelho.collidepoint(mouse_pos):
                    cor_fundo_atual = "#FD0E0E"
                if botao_fundo_azul.collidepoint(mouse_pos):
                    cor_fundo_atual = "#1F8BE4"
                if botao_fundo_cinza.collidepoint(mouse_pos):
                    cor_fundo_atual = "#6B7074"
                if botao_fundo_rosa.collidepoint(mouse_pos):
                    cor_fundo_atual = "#F4C2C2"

                if botao_botoes_vermelho.collidepoint(mouse_pos):
                    cores_botoes = "#FD0E0E"
                if botao_botoes_azul.collidepoint(mouse_pos):
                    cores_botoes = "#1F8BE4"
                if botao_botoes_roxo.collidepoint(mouse_pos):
                    cores_botoes = "#6503A6"
                if botao_botoes_branco.collidepoint(mouse_pos):
                    cores_botoes = "#FFFFFF"
                if botao_botoes_cinza.collidepoint(mouse_pos):
                    cores_botoes = "#6B7074"
                if botao_botoes_rosa.collidepoint(mouse_pos):
                    cores_botoes = "#F4C2C2"

                if botao_borda_vermelho.collidepoint(mouse_pos):
                    cor_borda_linhas_atual = "#FD0E0E"
                if botao_borda_azul.collidepoint(mouse_pos):
                    cor_borda_linhas_atual = "#1F8BE4"
                if botao_borda_roxo.collidepoint(mouse_pos):
                    cor_borda_linhas_atual = "#6503A6"
                if botao_borda_branco.collidepoint(mouse_pos):
                    cor_borda_linhas_atual = "#FFFFFF"
                if botao_borda_cinza.collidepoint(mouse_pos):
                    cor_borda_linhas_atual = "#6B7074"
                if botao_borda_rosa.collidepoint(mouse_pos):
                    cor_borda_linhas_atual = "#F4C2C2"
                if botao_borda_preto.collidepoint(mouse_pos):
                    cor_borda_linhas_atual = "#000000"
            if pagina_de_ajuda:
                if botao_voltar.collidepoint(mouse_pos):
                    pagina_inicial = True
                    pagina_configuracoes_aberta = True
                    pagina_de_ajuda = False
            if pagina_editar_aberta:
                if ticks_atuais - tempo_quando_abriu_editar >= 200:
                    if botao_voltar_editar.collidepoint(mouse_pos):
                        mostrar_botoes_laterais = True
                        pagina_editar_aberta = False
                    if pasta_aberta:
                        if botao_girar_foto.collidepoint(mouse_pos):
                            print(imagem_desenha)
                            posicao_giro = (posicao_giro + 1) % 4
                        if botao_desenho_foto.collidepoint(mouse_pos):
                            if imagem_desenha:
                                imagem_desenha = False
                            else:
                                imagem_desenha = True
                            abriu_primeira_aba_vez = False
                        if botao_desfoque_foto.collidepoint(mouse_pos):
                            if imagem_desfoque:
                                imagem_desfoque = False
                            else:
                                imagem_desfoque = True
                        if botao_espelhar_foto.collidepoint(mouse_pos):
                            if imagem_espelhada:
                                imagem_espelhada = False
                            else:
                                imagem_espelhada = True
                        if botao_vinheta_foto.collidepoint(mouse_pos):
                            if imagem_vinheta:
                                imagem_vinheta = False
                            else:
                                imagem_vinheta = True
                        if botao_resetar_foto.collidepoint(mouse_pos):
                            resetar_imagem()
                        if botao_aleatorizar_foto.collidepoint(mouse_pos):
                            aleatorizar_efeitos()
            if pagina_ler_aberta:
                if botao_voltar_editar.collidepoint(mouse_pos):
                    pagina_ler_aberta = False
                    pagina_inicial = True
                    mostrar_botoes_laterais = True
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                if indice_musica == 0:
                    indice_musica = 1
                else:
                    indice_musica = 0
                nome_musica_atual, caminho_musica_atual = tocar_musica(indice_musica)
                pygame.mixer.music.load(caminho_musica_atual)
                pygame.mixer.music.play(-1)
                musica_tocando = True
            if pagina_inicial:
                if pasta_aberta:
                    if event.key == pygame.K_SPACE:
                            aleatorizar(numero_fotos, indice_foto_atual)
                            ticks_clicou_randozimar = pygame.time.get_ticks()
                            clicou_botao_randomizar = True
                    if event.key == pygame.K_a:
                        lista_fotos_antigas = lista_fotos
                        embaralhar_fotos(lista_fotos)
                    if event.key == pygame.K_s:
                        numero_fotos, lista_fotos = listar_fotos(caminho)
                    if event.key == pygame.K_1:
                        indice_foto_atual = 0
                    if event.key == pygame.K_2: 
                        indice_foto_atual = numero_fotos - 1
            if event.key == pygame.K_l:
                if pagina_de_ajuda is False:
                    pagina_de_ajuda = True
                    pagina_inicial = False
                    pagina_configuracoes_aberta = False
                    pagina_personalisar_galeria_aberta = False
                else:
                    pagina_de_ajuda = False
                    pagina_inicial = True
                    mostrar_botoes_laterais = True
            if event.key == pygame.K_r:
                if pasta_aberta:
                    resetar_imagem()
            if event.key == pygame.K_RIGHT:
                if pasta_aberta:
                    if indice_foto_atual== numero_fotos - 1:
                        indice_foto_atual = 0
                    else:
                        indice_foto_atual += 1
            if event.key == pygame.K_LEFT:
                if pasta_aberta:
                    if indice_foto_atual - 1 == -1:
                        indice_foto_atual = numero_fotos - 1
                    else:
                        indice_foto_atual -= 1
            if event.key == pygame.K_m:
                if musica_tocando:
                    pygame.mixer.music.pause()
                    musica_tocando = False
                else:
                    pygame.mixer.music.unpause()
                

    screen.fill(cor_fundo_atual)
    keys = pygame.key.get_pressed()
    tempo_atual = pygame.time.get_ticks()

    if pagina_inicial:
        if pasta_aberta:
            surface = transformar_tamanho_imagem(lista_fotos[indice_foto_atual])
            i= pygame_para_pillow(surface)
            screen.blit(aplicar_efeitos(i), coordenada_desenhar_imagens)
            mostrar_numero_foto_atual(indice_foto_atual)
            if clicou_botao_randomizar:
                if (ticks_atuais - ticks_clicou_randozimar >= 1000):
                    clicou_botao_randomizar = False
                indice_foto_atual = aleatorizar(numero_fotos, indice_foto_atual)
        else:
            texto_botao_abrir_pasta = mostrar_botao_abrir_pasta()

        ticks_atuais = pygame.time.get_ticks()
        
        pygame.draw.rect(screen, cor_borda_linhas_atual, quadrado, 4)
        screen.blit(seta_direita, posicao_seta_direita)
        screen.blit(seta_esquerda, posicao_seta_esqurda)
        screen.blit(ponto_interrogacao, posicao_ponto_interrogacao)

        if mostrar_botoes_laterais:
            abriu_primeira_aba_vez = False
            funcao_mostrar_botoes_laterais()
        
        if pagina_configuracoes_aberta:
            funcao_mostrar_pagina_configuracoes()

        if pagina_editar_aberta:
            funcao_mostrar_pagina_editar_imagens()
    elif pagina_personalisar_galeria_aberta:
        funcao_pagina_personalisar()
    elif pagina_de_ajuda:
        funcao_mostrar_pagina_ajuda()
    elif pagina_ler_aberta:
        funcao_mostrar_pagina_ler()

    pygame.display.flip()

    clock.tick(25)

pygame.quit()