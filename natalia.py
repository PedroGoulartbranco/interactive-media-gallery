import pygame
from utils import *
from quadrados import *

pygame.init()
LARGURA, ALTURA = 1000, 600
screen = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

caminho = None

cores_botoes = "#6503A6"

pygame.display.set_caption("Te Amo Natalia")
fonte = pygame.font.SysFont('consolas', 20)

imagem_coracao = pygame.image.load(caminho_recurso("coracao_icon.png")).convert_alpha()
imagem_coracao = pygame.transform.scale(imagem_coracao, (128, 128))
pygame.display.set_icon(imagem_coracao)

pygame.mixer.init()

tempo_para_segurar = 250 #Tempo de cooldown para um clique nao contar como dois
ultimo_click = 0

pasta_aberta = False
mostrar_botoes_laterais = True
pagina_configuracoes_aberta = False
pagina_editar_aberta = False
pagina_ler_aberta = False
pagina_supresa_aberta = False

abriu_primeira_vez_configuracoes = False

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

    x_pos = (600 * escala_x) + (70 * escala_x)

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
    botao_voltar.y = (260 + 80) * escala_y

    botao_trocar_musica.width = nova_largura
    botao_trocar_musica.height = nova_altura
    botao_trocar_musica.x = x_pos
    botao_trocar_musica.y = (60 + 80) * escala_y

    botao_personalizar.width = nova_largura
    botao_personalizar.height = nova_altura
    botao_personalizar.x = x_pos
    botao_personalizar.y = (160 + 80) * escala_y

def atualizar_tamanho_quadrado(largura, altura):
    global coordenada_desenhar_imagens
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


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            atualizar_tamanho(event.w, event.h)
            atualizar_tamanho_quadrado(event.w, event.h)
            atualizar_botoes_de_imagem(event.w, event.h)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
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
                    mostrar_botoes_laterais = False
                if botao_ler.collidepoint(mouse_pos):
                    mostrar_botoes_laterais = False
                if botao_supresa.collidepoint(mouse_pos):
                    mostrar_botoes_laterais = False
            #Se a pagina de configurações estiver aberta
            if pagina_configuracoes_aberta:
                if abriu_primeira_vez_configuracoes is False:
                    abriu_primeira_vez_configuracoes = True
                else:
                    abriu_primeira_vez_configuracoes = False
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
                if botao_abrir_nova_pasta.collidepoint(mouse_pos) and abriu_primeira_vez_configuracoes  is False:
                    caminho_novo = abrir_pasta()
                    if verificar_pasta(caminho_novo):
                        pasta_aberta = True
                        caminho = caminho_novo
                        numero_fotos, lista_fotos = listar_fotos(caminho)
                        if numero_fotos == 0:
                            pasta_aberta = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                if indice_musica == 0:
                    indice_musica = 1
                else:
                    indice_musica = 0
                nome_musica_atual, caminho_musica_atual = tocar_musica(indice_musica)
                pygame.mixer.music.load(caminho_musica_atual)
                pygame.mixer.music.play(-1)
            if event.key == pygame.K_SPACE:
                if pasta_aberta:
                    aleatorizar(numero_fotos, indice_foto_atual)
                    ticks_clicou_randozimar = pygame.time.get_ticks()
                    clicou_botao_randomizar = True
                

    screen.fill("#AC01F4")
    keys = pygame.key.get_pressed()
    tempo_atual = pygame.time.get_ticks()
    
    if pasta_aberta:
        i = transformar_tamanho_imagem(lista_fotos[indice_foto_atual])
        screen.blit(i, coordenada_desenhar_imagens)
        mostrar_numero_foto_atual(indice_foto_atual)
        if clicou_botao_randomizar:
            if (ticks_atuais - ticks_clicou_randozimar >= 1000):
                clicou_botao_randomizar = False
            indice_foto_atual = aleatorizar(numero_fotos, indice_foto_atual)
    else:
        texto_botao_abrir_pasta = mostrar_botao_abrir_pasta()

    ticks_atuais = pygame.time.get_ticks()
    
    pygame.draw.rect(screen, "BLACK", quadrado, 4)
    screen.blit(seta_direita, posicao_seta_direita)
    screen.blit(seta_esquerda, posicao_seta_esqurda)
    screen.blit(ponto_interrogacao, posicao_ponto_interrogacao)
    
    if keys[pygame.K_LEFT]:
        if pasta_aberta:
            if tempo_atual - ultimo_click > tempo_para_segurar:
                ultimo_click = tempo_atual
                if indice_foto_atual - 1 == -1:
                    indice_foto_atual = numero_fotos - 1
                else:
                    indice_foto_atual -= 1
    if keys[pygame.K_RIGHT]:
        if tempo_atual - ultimo_click > tempo_para_segurar:
            ultimo_click = tempo_atual
            if pasta_aberta:
                if indice_foto_atual== numero_fotos - 1:
                    indice_foto_atual = 0
                else:
                    indice_foto_atual += 1

    if mostrar_botoes_laterais:
        abriu_primeira_vez_configuracoes = False
        funcao_mostrar_botoes_laterais()
    
    if pagina_configuracoes_aberta:
        funcao_mostrar_pagina_configuracoes()

    pygame.display.flip()

    clock.tick(25)

pygame.quit()