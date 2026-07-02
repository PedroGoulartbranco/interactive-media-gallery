import pygame
from utils import *
from quadrados import *
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops, ImageDraw
from random import choice
from matrizes_cores import *
from classes_jogos import Balao, TextoPontos

pygame.init()
LARGURA, ALTURA = 1000, 600
screen = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(400, 150)

caminho = None 
musica_tocando = True

dados_salvos = pegar_configuracoes_salvas()

largura_atual = LARGURA
altura_atual = ALTURA

i = None
angulo_atual = 0
imagem_girada = False
imagem_foi_girada_alguma_vez = False
contador_mudancas = 0

lista_imagens_pil = []

imagem_vermelho = False
imagem_branca = False
imagem_roxa = False
imagem_amarela = False
imagem_azul = False
imagem_verde = False
imagem_rosa = False
imagem_preto = False
imagem_laranja = False
imagem_verde_menta = False
imagem_preto_branco = False
imagem_psicodelico = False
imagem_polaroid = False
imagem_raioX = False

pygame.display.set_caption("Nossa Galeria")
fonte = pygame.font.SysFont('consolas', 20)

imagem_coracao = pygame.image.load(caminho_recurso("imagens/coracao_icon.png")).convert_alpha()
imagem_coracao = pygame.transform.scale(imagem_coracao, (128, 128))
pygame.display.set_icon(imagem_coracao)

pygame.mixer.init()

som_estouro = pygame.mixer.Sound(caminho_recurso("sons/som_estouro.ogg"))
som_estouro.set_volume(1.0)

tempo_para_segurar = 230 #Tempo de cooldown para um clique nao contar como dois
ultimo_click = 0

pasta_aberta = False
mostrar_botoes_laterais = True
pagina_configuracoes_aberta = False
pagina_editar_aberta = False
pagina_ler_aberta = False
pagina_supresa_aberta = False
pagina_de_ajuda = False
pagina_de_cores = False
pagina_extra_aberta = False

modo_jogo = False
em_contagem = False
jogo_comecou = False
ticks_clicou_em_jogar = 0
ticks_acabou_contagem = 0
contador_jogo = 3
trocou_para_musica_jogo = False
mosntrou_mensagem_jogo = False
tamanho_letra_aviso_jogo = 60
jogo_acabou = False
tela_rank = False
tela_salvar_nome = False
pegou_rank_do_json = False

modo_digitar = False
nome_jogador = ""

balao_azul = caminho_recurso("imagens/balao_azul.png")
balao_vermelho = caminho_recurso("imagens/balao_vermelho.png")
balao_roxo= caminho_recurso("imagens/balao_roxo.png")
balao_amarelo = caminho_recurso("imagens/balao_amarelo.png")

balao_azul = pygame.image.load(balao_azul).convert_alpha()
balao_vermelho = pygame.image.load(balao_vermelho).convert_alpha()
balao_roxo = pygame.image.load(balao_roxo).convert_alpha()
balao_amarelo = pygame.image.load(balao_amarelo).convert_alpha()

lista_baloes = [balao_amarelo, balao_roxo, balao_azul, balao_vermelho]

maximo_baloes = 20
tempo_maximo_jogo =  30000
baloes_podem_aparecer = False
pontuacao = 0
ticks_baloes_começaram_aparecer = 0
baloes_estourados = 0
posicao_rank = 0

grupo_balao = pygame.sprite.Group()
grupo_pontuacao = pygame.sprite.Group()

cores_botoes = dados_salvos["cor_botoes"]
cor_fundo_atual = dados_salvos["cor_fundo"]
cor_borda_linhas_atual = dados_salvos["cor_borda"]
caminho = dados_salvos["caminho"]

numero_fotos = lista_fotos = None

tick_quando_entrou_aba = 0
tempo_delay_botao = 150

if caminho == "":
    caminho = None
else:
    print(caminho)
    pasta_aberta = True
    numero_fotos, lista_fotos = listar_fotos(caminho)
    if numero_fotos == 0:
        pasta_aberta = False
 
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
indice_foto_atual = 0
ponto_interrogacao = pygame.image.load(caminho_recurso("imagens/interrogacao.png")).convert_alpha()
ponto_interrogacao = pygame.transform.scale(ponto_interrogacao, (100, 100))

seta_direita = pygame.image.load(caminho_recurso("imagens/seta.png")).convert_alpha()
seta_direita = pygame.transform.scale(seta_direita, (100, 100))

seta_esquerda = pygame.image.load(caminho_recurso("imagens/seta.png")).convert_alpha()
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
botao_branco = botao_vermelho = botao_roxo = botao_amarelo = botao_azul = botao_verde = botao_rosa =  botao_preto = botao_laranja = botao_verde_menta =  pygame.Rect(1 + 60, 0, 40, 40)


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
    fonte_atual = calculo_tamanho_fonte_atual(20)
    texto_botao_configuracoes = fonte_atual.render("Configurações", True, "black")
    texto_botao_editar = fonte_atual.render("Editar", True, "black")
    texto_botao_ler = fonte_atual.render("Leitura", True, "black")
    texto_botao_supresa = fonte_atual.render("Mais", True, "black")
    texto_jogo = fonte_atual.render("Jogar", True, "black")

    escala_x = largura_atual / LARGURA
    escala_y = altura_atual / ALTURA

    largura_quadrado =LARGURA_BOTOES * escala_x
    altura_quadrado = ALTURA_BOTOES * escala_y

    x_pos = DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES * escala_x
    
    ys_originais = [
        30,
        60 + ALTURA_BOTOES,
        160 + ALTURA_BOTOES,
        260 + ALTURA_BOTOES,
        360 + ALTURA_BOTOES
    ]

    for i, botao in enumerate(lista_botoes_principais):
        botao.width = largura_quadrado
        botao.height = altura_quadrado
        botao.x = x_pos
        botao.y = ys_originais[i] * escala_y
        pygame.draw.rect(screen, cores_botoes, botao)

    dicionario_coordenadas = {
        texto_botao_configuracoes:  texto_botao_configuracoes.get_rect(center=botao_configuracoes.center),
        texto_botao_editar: texto_botao_editar.get_rect(center=botao_editar_imagens.center),
        texto_botao_ler: texto_botao_ler.get_rect(center=botao_ler.center),
        texto_botao_supresa: texto_botao_supresa.get_rect(center=botao_supresa.center),
        texto_jogo: texto_jogo.get_rect(center=botao_jogar.center)
    }

    for texto in dicionario_coordenadas:
            screen.blit(texto, dicionario_coordenadas[texto])


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

    nova_largura_botoes_menores = 150 * escala_x
    nova_altura_botoes_menores = 80 * escala_y

    x_pos = DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES * escala_x
    x_pos_botoes_menores = (300 * escala_x) + (70 * escala_x)
    x_pos_botoes_medios = (150 * escala_x) + (80 * escala_x)

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

    botao_polaroid.width = (LARGURA_BOTOES * 0.5) * escala_x
    botao_polaroid.height = ALTURA_BOTOES_EDITAR * escala_y
    botao_polaroid.x = DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES * escala_x
    botao_polaroid.y = 150 * escala_y

    botao_preto_branco.width = (LARGURA_BOTOES * 0.5) * escala_x
    botao_preto_branco.height = (ALTURA_BOTOES_EDITAR) * escala_y
    botao_preto_branco.x = (DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES * escala_x + botao_polaroid.width + (20 * escala_x))
    botao_preto_branco.y = botao_polaroid.y

    botao_raio_x.width = (LARGURA_BOTOES * 0.5) * escala_x
    botao_raio_x.height = ALTURA_BOTOES_EDITAR * escala_y
    botao_raio_x.x = DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES * escala_x
    botao_raio_x.y =  botao_polaroid.y + botao_polaroid.height + (30 * escala_y)

    botao_psicodelico.width = (LARGURA_BOTOES * 0.5) * escala_x
    botao_psicodelico.height = (ALTURA_BOTOES_EDITAR) * escala_y
    botao_psicodelico.x = (DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES * escala_x + botao_raio_x.width + (20 * escala_x))
    botao_psicodelico.y = botao_raio_x.y

    botao_resetar_cores.width = (botao_vinheta_foto.width + (20 * escala_x) + botao_espelhar_foto.width)
    botao_resetar_cores.height = nova_altura
    botao_resetar_cores.x = x_pos
    botao_resetar_cores.y = (botao_raio_x.y + botao_raio_x.height + (20 * escala_y))

    botao_voltar_cores.width = (botao_vinheta_foto.width + (20 * escala_x) + botao_espelhar_foto.width)
    botao_voltar_cores.height = nova_altura
    botao_voltar_cores.x = x_pos
    botao_voltar_cores.y = (botao_resetar_cores.y + botao_resetar_cores.height + (20 * escala_y))
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

    texto = """<  ===> Ir para a imagem da esquerda, você pode segurar esse botão\n> ===> Ir para a imagem da direita, você pode segurar esse botão\n1 ===> Ir para primeira imagem\n2 ===> Ir para ultima imagem\nSpace ===> Escolher uma foto aleatoria\nA ===> Embaralhar as fotos\nS ===> Desembaralhar as fotos\n↑ ===> Trocar de música\n↓ ===> Trocar de música\nL ===> Abrir página de ajuda\nR ===> Resetar Imagem (Deixar ela original)\nP ===> Pausar Música
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
        img_temp = img_temp.convert("RGB")
        img_temp = ImageOps.invert(img_temp)
        img_temp = img_temp.convert("RGB", matriz_raiox)

    if imagem_vermelho is not False:
        img_temp = img_temp.convert("RGB", imagem_vermelho)
    if imagem_branca is not False:
        img_temp = img_temp.convert("RGB", imagem_branca)
    if imagem_roxa is not False:
        img_temp = img_temp.convert("RGB", imagem_roxa)
    if imagem_amarela is not False:
        img_temp = img_temp.convert("RGB", imagem_amarela)
    if imagem_azul is not False:
        img_temp = img_temp.convert("RGB", imagem_azul)
    if imagem_verde is not False:
        img_temp = img_temp.convert("RGB", imagem_verde)
    if imagem_rosa is not False:
        img_temp = img_temp.convert("RGB", imagem_rosa)
    if imagem_preto is not False:
        img_temp = img_temp.convert("RGB", imagem_preto)
    if imagem_laranja is not False:
        img_temp = img_temp.convert("RGB", imagem_laranja)
    if imagem_verde_menta is not False:
        img_temp = img_temp.convert("RGB", imagem_verde_menta)
    if imagem_preto_branco is not False:
        img_temp = img_temp.convert("RGB", imagem_preto_branco)
    if imagem_psicodelico is not False:
        img_temp = img_temp.convert("RGB", imagem_psicodelico)
    if imagem_polaroid is not False:
        img_temp = img_temp.convert("RGB", imagem_polaroid)


    modo = img_temp.mode
    tamanho = img_temp.size
    dados = img_temp.tobytes()
   
    return pygame.image.fromstring(dados, tamanho, modo)

def resetar_imagem():
    global imagem_raioX, imagem_desenha, imagem_espelhada, posicao_giro, imagem_desfoque, imagem_vinheta


    imagem_vinheta = imagem_raioX = imagem_desenha = imagem_espelhada =imagem_desfoque = False
    posicao_giro = 0
    resetar_cores_efeitos()

def resetar_cores_efeitos():
    global imagem_vermelho, imagem_branca, imagem_amarela, imagem_azul, imagem_roxa, imagem_verde
    global imagem_rosa, imagem_preto, imagem_laranja, imagem_verde_menta, imagem_preto_branco
    global imagem_psicodelico, imagem_polaroid, imagem_raioX

    imagem_vermelho = False
    imagem_branca = False
    imagem_roxa = False
    imagem_amarela = False
    imagem_azul = False
    imagem_verde = False
    imagem_rosa = False
    imagem_preto = False
    imagem_laranja = False
    imagem_verde_menta = False
    imagem_preto_branco = False
    imagem_psicodelico = False
    imagem_polaroid = False
    imagem_raioX = False

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


def funcao_mostrar_botoes_cores():
    escala_x = largura_atual / LARGURA
    escala_y = altura_atual / ALTURA
    distancia_base = (quadrado.width + (70 * escala_x))

    global botao_branco, botao_vermelho, botao_roxo, botao_amarelo, botao_azul, botao_verde, botao_rosa, botao_preto
    global botao_laranja, botao_verde_menta, DISTANCIA_PAREDE_BOTOES_COR
    fonte_atual = calculo_tamanho_fonte_atual(20)
    texto_botao_voltar = fonte_atual.render("Voltar", True, "black")

    DISTANCIA_PAREDE_BOTOES_COR =  quadrado.width + 70

    distancia_base = DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES * escala_x
    y_distancia_cor = 30 * escala_y

    largura_quadrado_cores =LARGURA_COR_ORIGINAL * escala_x
    altura_quadrado_cores = ALTURA_COR_ORIGINAL * escala_y

    dis_70 = 70 * escala_x
    dis_140 = 140 * escala_x
    dis_210 = 210 * escala_x
    dis_280 = 280 * escala_x

    #Fundo
    botao_branco = pygame.Rect(distancia_base, y_distancia_cor, largura_quadrado_cores, altura_quadrado_cores)
    botao_vermelho = pygame.Rect(distancia_base + dis_70, y_distancia_cor, largura_quadrado_cores, altura_quadrado_cores)
    botao_roxo = pygame.Rect(distancia_base + dis_140, y_distancia_cor, largura_quadrado_cores, altura_quadrado_cores)
    botao_amarelo = pygame.Rect(distancia_base + dis_210, y_distancia_cor, largura_quadrado_cores, altura_quadrado_cores)
    botao_azul = pygame.Rect(distancia_base + dis_280, y_distancia_cor, largura_quadrado_cores, altura_quadrado_cores)
    botao_verde  = pygame.Rect(distancia_base, y_distancia_cor + botao_branco.height + 10, largura_quadrado_cores, altura_quadrado_cores)
    botao_rosa = pygame.Rect(distancia_base + dis_70, y_distancia_cor + botao_branco.height + 10, largura_quadrado_cores, altura_quadrado_cores)
    botao_preto = pygame.Rect(distancia_base + dis_140, y_distancia_cor + botao_branco.height + 10, largura_quadrado_cores, altura_quadrado_cores)
    botao_laranja = pygame.Rect(distancia_base + dis_210, y_distancia_cor + botao_branco.height + 10, largura_quadrado_cores, altura_quadrado_cores)
    botao_verde_menta = pygame.Rect(distancia_base + dis_280, y_distancia_cor + botao_branco.height + 10, largura_quadrado_cores, altura_quadrado_cores)
    
    dicionario_cor = {
        "#FFFFFF": botao_branco,
        "#FD0E0E": botao_vermelho,
        "#6503A6": botao_roxo,
        "#ffee00": botao_amarelo,
        "#1F8BE4": botao_azul,
        "#3bfc00": botao_verde,
        "#c958d3": botao_rosa,
        "#000000": botao_preto,
        "#f36f03": botao_laranja,
        "#8CDCC8": botao_verde_menta
    }

    for botao in dicionario_cor:
        pygame.draw.rect(screen, botao, dicionario_cor[botao])

    fonte_atual = calculo_tamanho_fonte_atual(17)
    fonte_segunda = calculo_tamanho_fonte_atual(20)

    texto_polaroid = fonte_atual.render("Polaroid", True, "black")
    texto_preto_branco = fonte_atual.render("Preto e Branco", True, "black")
    texto_raio_x = fonte_atual.render("Raio X", True, "black")
    texto_psicodelico = fonte_atual.render("Psicodélico", True, "black")
    texto_resetar_cor = fonte_segunda.render("Resetar Cores", True, "black")

    dicionario_texto_botoes = {
        texto_polaroid:  texto_polaroid.get_rect(center=botao_polaroid.center),
        texto_preto_branco: texto_preto_branco.get_rect(center=botao_preto_branco.center),
        texto_raio_x: texto_raio_x.get_rect(center=botao_raio_x.center),
        texto_psicodelico: texto_psicodelico.get_rect(center=botao_psicodelico.center),
        texto_resetar_cor: texto_resetar_cor.get_rect(center=botao_resetar_cores.center),
        texto_botao_voltar: texto_botao_voltar.get_rect(center=botao_voltar_cores.center)
    }

    for botao in lista_botoes_especiais_editar:
        pygame.draw.rect(screen, cores_botoes, botao)

    for texto in dicionario_texto_botoes:
        screen.blit(texto, dicionario_texto_botoes[texto])

def funcao_mostrar_pagina_mais():
    fonte_atual = calculo_tamanho_fonte_atual(20)
    texto_botao_salvar_caminho = fonte_atual.render("Salvar Pasta", True, "black")
    texto_botao_limpar = fonte_atual.render("Limpar Caminho", True, "black")
    texto_botao_salvar_imagem = fonte_atual.render("Baixar Imagem", True, "black")
    texto_botao_salvar_edicoes = fonte_atual.render("Salvar Edições", True, "black")
    texto_botao_voltar = fonte_atual.render("Voltar", True, "black")

    escala_x = largura_atual / LARGURA
    escala_y = altura_atual / ALTURA

    largura_quadrado =LARGURA_BOTOES * escala_x
    altura_quadrado = ALTURA_BOTOES * escala_y

    x_pos = DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES * escala_x
    
    ys_originais = [
        30,
        60 + ALTURA_BOTOES,
        160 + ALTURA_BOTOES,
        260 + ALTURA_BOTOES,
        360 + ALTURA_BOTOES
    ]

    for i, botao in enumerate(lista_botoes_mais):
        botao.width = largura_quadrado
        botao.height = altura_quadrado
        botao.x = x_pos
        botao.y = ys_originais[i] * escala_y
        pygame.draw.rect(screen, cores_botoes, botao)


    dicionario_texto_botoes = {
        texto_botao_salvar_caminho: texto_botao_salvar_caminho.get_rect(center=botao_salvar_caminho_pasta.center),
        texto_botao_limpar: texto_botao_limpar.get_rect(center=botao_limpar_caminho_pasta.center),
        texto_botao_salvar_edicoes: texto_botao_salvar_edicoes.get_rect(center=botao_salvar_edicoes.center),
        texto_botao_voltar: texto_botao_voltar.get_rect(center=botao_voltar_extra.center),
        texto_botao_salvar_imagem: texto_botao_salvar_imagem.get_rect(center=botao_baixar_imagem.center)
    }

    for texto in dicionario_texto_botoes:
        screen.blit(texto, dicionario_texto_botoes[texto])


def contagem_jogo():
    global contador_jogo, ticks_clicou_em_jogar
    tempo_atual = pygame.time.get_ticks()
    fonte_atual = calculo_tamanho_fonte_atual(100)
    texto_aviso = fonte_atual.render("Estoure o maximo de balões", True, "black")

    centro_tela_x = int(LARGURA / 2)
    centro_tela_y = int(ALTURA / 2)

    if tempo_atual - ticks_clicou_em_jogar >= 1000:
        contador_jogo -= 1
        ticks_clicou_em_jogar = tempo_atual

        if contador_jogo == 0:
            return True
    texto = fonte_atual.render(str(contador_jogo), True, "black")
    rect_texto = texto.get_rect(center=(centro_tela_x, centro_tela_y))
    screen.blit(texto, rect_texto)
    print(contador_jogo)

    return False

def mostrar_mensagem_baloes(ticks_acabou_contagem):
    global tamanho_letra_aviso_jogo
    tempo_atual = pygame.time.get_ticks()
    fonte_atual = calculo_tamanho_fonte_atual(tamanho_letra_aviso_jogo)
    texto_aviso = fonte_atual.render("Estoure o maximo de balões", True, "black")

    centro_tela_x = int(LARGURA / 2)
    centro_tela_y = int(ALTURA / 2)

    if tempo_atual - ticks_acabou_contagem <= 2000:
        print(tempo_atual - ticks_acabou_contagem)
        rect_texto = texto_aviso.get_rect(center=(centro_tela_x, centro_tela_y))
        screen.blit(texto_aviso, rect_texto)
        tamanho_letra_aviso_jogo -= 1.5
        return False
    return True

def calcular_largura_altura_janela():
    largura = screen.get_width()


    altura = screen.get_height()

    return largura, altura

def desenhar_pontuacao_e_tempo(pontuacao, tick_quando_comecou):
    tempo_atual = pygame.time.get_ticks()
    fonte_atual = calculo_tamanho_fonte_atual(20)
    texto_surface =  fonte_atual.render(f"Pontos: {pontuacao}", True, "black")
    largura_tela = screen.get_width()

    texto_rect = texto_surface.get_rect()
    
    margem = 20  
    texto_rect.topright = (largura_tela - margem, margem)

    segundos = 30 - ((tempo_atual - tick_quando_comecou) // 1000)
    texto_segundos =  fonte_atual.render(f"Tempo: {segundos}s", True, "black")
    texto_segundos_rect = texto_segundos.get_rect()
    texto_segundos_rect.topright = (largura_atual - margem, margem + texto_rect.y)

    screen.blit(texto_surface, texto_rect)
    screen.blit(texto_segundos, texto_segundos_rect)

def mensagem_fim_jogo(pontos, baloes_estourados):
    global rect_botao_salvar_nome, rect_quadrado_digitar, posicao_rank
    fonte_titulo = calculo_tamanho_fonte_atual(40)
    fonte_atual = calculo_tamanho_fonte_atual(30)
    titulo =  fonte_titulo.render("Fim de jogo", True, "black")
    texto_informacoes = [f"Pontos: {str(pontos)}",
                         f"Balões estourados: {str(baloes_estourados)}"]
    largura_tela = screen.get_width()
    titulo_rect = titulo.get_rect()
    margem = 20 
    titulo_rect.midtop = (largura_tela // 2, margem)

    y_atual = titulo_rect.bottom + margem

    for linha in texto_informacoes:
        texto_surf = fonte_atual.render(linha, True, "black")
        rect_texto = texto_surf.get_rect()
        rect_texto.midtop = (largura_tela // 2, y_atual)

        screen.blit(texto_surf, rect_texto)

        y_atual += rect_texto.height + 10

    posicao_rank = calcular_posicao_jogador_rank(pontos)
    if int(posicao_rank)  == 0 or int(posicao_rank) == 6:
        texto_rank = fonte_atual.render(f"Você está fora do Rank!", True, "black")
        texto_fechar = fonte_atual.render("Fechar", True, "black")

        rect_texto_rank = texto_rank.get_rect()

        rect_texto_rank.midtop = ((largura_tela // 2, y_atual + 20))

        screen.blit(texto_rank, rect_texto_rank)
        rect_botao_sair_tela_pontuacao.midtop = (largura_tela // 2, rect_texto_rank.y + 150)
        pygame.draw.rect(screen, cores_botoes, rect_botao_sair_tela_pontuacao)

        rect_texto_botao_fechar = texto_fechar.get_rect(center=rect_botao_sair_tela_pontuacao.center)
        screen.blit(texto_fechar, rect_texto_botao_fechar)

    else:
        texto_rank = fonte_atual.render(f"Você está em {posicao_rank}º no Rank!", True, "black")
        texto_salvar = fonte_atual.render("Salvar", True, "black")
        texto_nome = fonte_atual.render(str(nome_jogador), True, "black")

        rect_texto_rank = texto_rank.get_rect()

        rect_texto_rank.midtop = ((largura_tela // 2, y_atual + 20))

        screen.blit(texto_rank, rect_texto_rank)

        # rect_quadrado_digitar = pygame.Rect(0, 0, 300, 50)
        # rect_botao_salvar_nome = pygame.Rect(0, 0, 200, 50)
        
        rect_quadrado_digitar.midtop = (largura_tela // 2, rect_texto_rank.y + 100)
        rect_botao_salvar_nome.midtop = (largura_tela // 2, rect_quadrado_digitar.y + 100)
        
        pygame.draw.rect(screen, "#e4c1c1", rect_quadrado_digitar)
        pygame.draw.rect(screen, cores_botoes, rect_botao_salvar_nome)

        rect_texto_botao_salvar = texto_salvar.get_rect(center=rect_botao_salvar_nome.center)
        screen.blit(texto_salvar, rect_texto_botao_salvar)

        rect_nome_jogador = texto_nome.get_rect(center=rect_quadrado_digitar.center)

        screen.blit(texto_nome, rect_nome_jogador)
    screen.blit(titulo, titulo_rect)

def funcao_mostrando_rank():
    global pegou_rank_do_json, botao_sair_jogo
    fonte_titulo = calculo_tamanho_fonte_atual(50)
    fonte_atual = calculo_tamanho_fonte_atual(30)
    titulo = fonte_titulo.render(f"Rank", True, "black")

    largura_tela = screen.get_width()
    titulo_rect = titulo.get_rect()
    margem = 20 
    titulo_rect.midtop = (largura_tela // 2, margem)

    screen.blit(titulo, titulo_rect)

    dados_rank = pegar_pontuacao_no_rank()

    y_atual = 100
    posicao_x_fixa = (largura_tela // 2) - 150

    coluna_nome = (largura_tela // 2) -200
    coluna_pontos = (largura_tela // 2) + 200

    for i in range(1, 6):
        texto_nome = fonte_atual.render(f"{i} - {dados_rank[str(i)]["nome"]}", True, "black")
        texto_pontos = fonte_atual.render(f"{dados_rank[str(i)]["pontos"]}pts", True, "black")
    
        rect_nome = texto_nome.get_rect()
        rect_pontos = texto_pontos.get_rect()

        rect_nome.topleft = (coluna_nome, y_atual)
        
        rect_pontos.topright = (coluna_pontos, y_atual)


        screen.blit(texto_nome, rect_nome)
        screen.blit(texto_pontos, rect_pontos)

        y_atual += rect_nome.height + 20

        if dados_rank[str(i)]["nome"] == nome_jogador and dados_rank[str(i)]["pontos"] == pontuacao:
            largura_borda = coluna_nome - coluna_pontos - 40
            altura_borda = rect_nome.height + 15

            rect_borda = pygame.Rect(0, 0, largura_borda, altura_borda)

            rect_borda.center = ((coluna_nome + coluna_pontos)// 2, rect_nome.centery)
            pygame.draw.rect(screen, "black", rect_borda, 2, border_radius=5)

    escala_x = largura_atual / LARGURA
    escala_y = altura_atual / ALTURA

    largura_botao =LARGURA_BOTOES * escala_x
    altura_botao = ALTURA_BOTOES * escala_y
    botao_sair_jogo = pygame.Rect(0, 0, largura_botao, altura_botao)
    botao_sair_jogo.midtop = (largura_tela // 2, y_atual + 50)
    pygame.draw.rect(screen, cores_botoes, botao_sair_jogo)

    texto_sair = fonte_atual.render("Sair", True, "black")
    rect_texto_sair = texto_sair.get_rect(center=botao_sair_jogo.center)

    screen.blit(texto_sair, rect_texto_sair)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            atualizar_tamanho_quadrado(event.w, event.h)
            atualizar_tamanho(event.w, event.h)
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
                    print("aaa")
                    pagina_extra_aberta = True
                    mostrar_botoes_laterais = False
                if botao_jogar.collidepoint(mouse_pos):
                    mostrar_botoes_laterais = False
                    pagina_inicial = False
                    modo_jogo = True
                    em_contagem = True
                    ticks_clicou_em_jogar = tempo_atual
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
                        if botao_cores_foto.collidepoint(mouse_pos):
                            tick_quando_entrou_aba = tempo_atual
                            pagina_inicial = True
                            pagina_editar_aberta = False
                            mostrar_botoes_laterais = False
                            pagina_de_cores = True
            if pagina_ler_aberta:
                if botao_voltar_editar.collidepoint(mouse_pos):
                    pagina_ler_aberta = False
                    pagina_inicial = True
                    mostrar_botoes_laterais = True
            if pagina_de_cores:
                if tempo_atual - tick_quando_entrou_aba >= tempo_delay_botao:
                    if botao_vermelho.collidepoint(mouse_pos):
                        if imagem_vermelho is False:
                            imagem_vermelho = matriz_vermelho

                        else:
                            imagem_vermelho = False
                    if botao_branco.collidepoint(mouse_pos):
                        if imagem_branca is False:
                            imagem_branca = matriz_branca
                        else:
                            imagem_branca = False
                    if botao_roxo.collidepoint(mouse_pos):
                        if imagem_roxa is False:
                            imagem_roxa = matriz_roxa
                        else:
                            imagem_roxa = False
                    if botao_amarelo.collidepoint(mouse_pos):
                        if imagem_amarela is False:
                            imagem_amarela = matriz_amarela
                        else:
                            imagem_amarela = False
                    if botao_azul.collidepoint(mouse_pos):
                        if imagem_azul is False:
                            imagem_azul = matriz_azul
                        else:
                            imagem_azul = False
                    if botao_verde.collidepoint(mouse_pos):
                        if imagem_verde is False:
                            imagem_verde = matriz_verde
                        else:
                            imagem_verde = False
                    if botao_rosa.collidepoint(mouse_pos):
                        if imagem_rosa is False:
                            imagem_rosa = matriz_rosa
                        else:
                            imagem_rosa = False
                    if botao_preto.collidepoint(mouse_pos):
                        if imagem_preto is False:
                            imagem_preto = matriz_preta
                        else:
                            imagem_preto = False
                    if botao_laranja.collidepoint(mouse_pos):
                        if imagem_laranja is False:
                            imagem_laranja = matriz_laranja
                        else:
                            imagem_laranja = False
                    if botao_verde_menta.collidepoint(mouse_pos):
                        if imagem_verde_menta is False:
                            imagem_verde_menta = matriz_verde_menta
                        else:
                            imagem_verde_menta = False
                if botao_preto_branco.collidepoint(mouse_pos):
                    if imagem_preto_branco is False:
                        imagem_preto_branco = matriz_preto_e_branco
                    else:
                        imagem_preto_branco = False
                if botao_psicodelico.collidepoint(mouse_pos):
                    if imagem_psicodelico is False:
                        imagem_psicodelico = matriz_psicodelica
                    else:
                        imagem_psicodelico = False
                if botao_polaroid.collidepoint(mouse_pos):
                    if imagem_polaroid is False:
                        imagem_polaroid = matriz_polaroid
                    else:
                        imagem_polaroid = False
                if botao_raio_x.collidepoint(mouse_pos):
                    if imagem_raioX:
                        imagem_raioX = False
                    else:
                        imagem_raioX = True
                if botao_resetar_cores.collidepoint(mouse_pos):
                    resetar_cores_efeitos()
                if botao_voltar_cores.collidepoint(mouse_pos):
                    pagina_de_cores = False
                    pagina_editar_aberta = True

            if pagina_extra_aberta:
                if abriu_primeira_aba_vez is False:
                    abriu_primeira_aba_vez = True
                else:
                    abriu_primeira_aba_vez = False
                if botao_voltar_extra.collidepoint(mouse_pos) and abriu_primeira_aba_vez is False:
                    mostrar_botoes_laterais = True
                    pagina_extra_aberta = False
                if botao_salvar_caminho_pasta.collidepoint(mouse_pos):
                    if caminho is not None:
                        salvar_caminho_json(caminho)
                if botao_limpar_caminho_pasta.collidepoint(mouse_pos):
                    limpar_caminho_json()
                if botao_salvar_edicoes.collidepoint(mouse_pos):
                    salvar_configuracoes_json(cor_fundo_atual, cores_botoes, cor_borda_linhas_atual)
                if botao_baixar_imagem.collidepoint(mouse_pos):
                    if i is not None:
                        print("oi")
                        baixar_imagem(i)
            if jogo_comecou:
                fonte_pontuacao_balao = calculo_tamanho_fonte_atual(20)
                for balao in reversed(grupo_balao.sprites()):
                    if balao.rect.collidepoint(mouse_pos):
                        rel_x = mouse_pos[0] - balao.rect.x
                        rel_y = mouse_pos[1] - balao.rect.y

                        if balao.mask.get_at((rel_x, rel_y)):
                            balao.kill() 
                            pontuacao += balao.pontos
                            texto_pontos = TextoPontos(f"+{balao.pontos}", mouse_pos[0], mouse_pos[1], fonte_pontuacao_balao)
                            grupo_pontuacao.add(texto_pontos)
                            som_estouro.play()
                            baloes_estourados += 1
                            break
            if jogo_acabou:
                if tela_salvar_nome:
                    if int(posicao_rank)  == 0 or int(posicao_rank) == 6:
                        if rect_botao_sair_tela_pontuacao.collidepoint(mouse_pos):
                            tela_salvar_nome = False
                            tela_rank = True
                    else:
                        if rect_quadrado_digitar.collidepoint(mouse_pos):
                            modo_digitar = True
                            pygame.key.start_text_input()
                            print(modo_digitar)
                        if rect_botao_salvar_nome.collidepoint(mouse_pos):
                            if len(nome_jogador) >= 1:
                                tela_salvar_nome = False
                                salvar_rank_json(nome_jogador, posicao_rank, pontuacao, baloes_estourados)
                                tela_rank = True
                                modo_digitar = False
                                pygame.key.stop_text_input()
            if tela_rank:
                if botao_sair_jogo.collidepoint(mouse_pos):
                    print("clicou")
                    jogo_acabou = False
                    tela_rank = False
                    nome_jogador = ""
                    pontuacao = 0
                    baloes_estourados = 0
                    pagina_inicial = True
                    mostrar_botoes_laterais = True
                    ticks_clicou_em_jogar = 0
                    ticks_acabou_contagem = 0
                    contador_jogo = 3
                    mosntrou_mensagem_jogo = False
                    trocou_para_musica_jogo = False
                    modo_jogo = False
                    nome_musica_atual, caminho_musica_atual = tocar_musica(indice_musica)
                    pygame.mixer.music.load(caminho_musica_atual)
                    pygame.mixer.music.play(-1)
        if modo_digitar:
            if event.type == pygame.TEXTINPUT:
                    print(event.text)
                    if len(nome_jogador) < 5:
                        nome_jogador += event.text
            if event.type  == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
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
            if modo_digitar is False:
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
                if event.key == pygame.K_p:
                    if musica_tocando:
                        pygame.mixer.music.pause()
                        musica_tocando = False
                    else:
                        pygame.mixer.music.unpause()
                        musica_tocando = True
                

    screen.fill(cor_fundo_atual)
    keys = pygame.key.get_pressed()
    tempo_atual = pygame.time.get_ticks()

    if pagina_inicial:
        if pasta_aberta:
            surface = transformar_tamanho_imagem(lista_fotos[indice_foto_atual])
            i= pygame_para_pillow(surface)
            i = aplicar_efeitos(i)
            screen.blit(i, coordenada_desenhar_imagens)
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
        elif pagina_de_cores:
            funcao_mostrar_botoes_cores()
        
        if pagina_configuracoes_aberta:
            funcao_mostrar_pagina_configuracoes()

        if pagina_editar_aberta:
            funcao_mostrar_pagina_editar_imagens()

        if pagina_extra_aberta:
            funcao_mostrar_pagina_mais()
    elif pagina_personalisar_galeria_aberta:
        funcao_pagina_personalisar()
    elif pagina_de_ajuda:
        funcao_mostrar_pagina_ajuda()
    elif pagina_ler_aberta:
        funcao_mostrar_pagina_ler()
    elif modo_jogo:
        if trocou_para_musica_jogo is False:
            pygame.mixer.music.load(retornar_caminho_musica_jogo())
            pygame.mixer.music.play(-1)
            trocou_para_musica_jogo = True
        if em_contagem:
            jogo_comecou = contagem_jogo()
            ticks_acabou_contagem = tempo_atual
            if jogo_comecou:
                em_contagem = False
        elif jogo_comecou:
            em_contagem = False
            pygame.mixer.music.set_volume(0.7)
            if mosntrou_mensagem_jogo is False:
                mosntrou_mensagem_jogo = mostrar_mensagem_baloes(ticks_acabou_contagem)
                baloes_podem_aparecer = True
                ticks_baloes_começaram_aparecer = tempo_atual

            if baloes_podem_aparecer:

                largura_atual_janela, altura_atual_janela = calcular_largura_altura_janela()
                
                if len(grupo_balao) < maximo_baloes:
                    balao_atual_cor = choice(lista_baloes)
                    novo_balao = Balao(balao_atual_cor, largura_atual_janela, altura_atual_janela)
                    grupo_balao.add(novo_balao)
        
                grupo_balao.update()
                grupo_balao.draw(screen)

                grupo_pontuacao.update()
                grupo_pontuacao.draw(screen)

                desenhar_pontuacao_e_tempo(pontuacao, ticks_baloes_começaram_aparecer)

                if tempo_atual - ticks_baloes_começaram_aparecer >= tempo_maximo_jogo:
                    print("acabou")
                    baloes_podem_aparecer = False
                    jogo_acabou = True
                    grupo_balao.empty()
                    grupo_pontuacao.empty()
                    tela_salvar_nome = True
            if jogo_acabou:
                if tela_salvar_nome:
                    mensagem_fim_jogo(pontuacao, baloes_estourados)
                if tela_rank:
                    funcao_mostrando_rank()
                
    pygame.display.flip()

    clock.tick(60)

pygame.quit()