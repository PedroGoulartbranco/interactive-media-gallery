import pygame


LARGURA_QUADRADO, ALTURA_QUADRADO = 600, 450
TEMPO_APARECER_NOME_MUSICA = 5000
DISTANCIA_LATERAL_QUADRADO = 50

DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES =  LARGURA_QUADRADO + 70
LARGURA_BOTOES, ALTURA_BOTOES = 300, 80
ALTURA_BOTOES_EDITAR = ALTURA_BOTOES
DISTANCIA_PAREDE_BOTOES_COR = 0
LARGURA_COR_ORIGINAL = 40 
ALTURA_COR_ORIGINAL = 40

quadrado_cinza = pygame.Rect(DISTANCIA_LATERAL_QUADRADO, 30, LARGURA_QUADRADO, ALTURA_QUADRADO)

#Criar Quadrados de menu
botao_configuracoes = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 30, LARGURA_BOTOES, ALTURA_BOTOES)
botao_editar_imagens = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 60 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)
botao_ler = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 160 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)
botao_supresa = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 260 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)
botao_jogar = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 360 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)
#Criar botao de voltar
botao_voltar = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 360 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)

#Menu de configurações
botao_abrir_nova_pasta = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 30, LARGURA_BOTOES, ALTURA_BOTOES)
botao_trocar_musica = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 60 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)
botao_personalizar = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 160 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)
botao_ajuda = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 260 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)

#Menu de editar
botao_girar_foto = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 30, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_cores_foto = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES + botao_girar_foto.width + 20, 30, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_desenho_foto = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 130, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_desfoque_foto = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES + botao_desenho_foto.width + 20, 130, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_vinheta_foto = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, botao_desfoque_foto.y + 100, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_espelhar_foto = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES + botao_vinheta_foto.width + 20, botao_desfoque_foto.y + 100, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_aleatorizar_foto = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, botao_vinheta_foto.y + 100, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_resetar_foto = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES + botao_desenho_foto.width + 20, botao_vinheta_foto.y + 100, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)

botao_voltar_editar =  pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, botao_aleatorizar_foto.y + 100, botao_vinheta_foto.width + 20 + botao_espelhar_foto.width, ALTURA_BOTOES_EDITAR)

lista_botoes_editar = [botao_girar_foto, botao_cores_foto, botao_desenho_foto, botao_desfoque_foto, botao_vinheta_foto, botao_espelhar_foto, botao_voltar_editar, botao_aleatorizar_foto, botao_resetar_foto]

#Botoes de cores painel cor
botao_polaroid = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 150, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_preto_branco = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES + botao_desenho_foto.width + 20, 150, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_raio_x = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, botao_desfoque_foto.y + 120, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)
botao_psicodelico = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES + botao_vinheta_foto.width + 20, botao_desfoque_foto.y + 120, LARGURA_BOTOES * 0.5, ALTURA_BOTOES_EDITAR)

botao_resetar_cores = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 260 + ALTURA_BOTOES, botao_vinheta_foto.width + 20 + botao_espelhar_foto.width, ALTURA_BOTOES)
botao_voltar_cores = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, botao_aleatorizar_foto.y + 100, botao_vinheta_foto.width + 20 + botao_espelhar_foto.width, ALTURA_BOTOES_EDITAR)

lista_botoes_especiais_editar = [botao_polaroid, botao_preto_branco, botao_raio_x, botao_psicodelico, botao_resetar_cores, botao_voltar_cores]

#Botões segundo menu
botao_salvar_caminho_pasta = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 30, LARGURA_BOTOES, ALTURA_BOTOES)
botao_limpar_caminho_pasta = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 60 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)
botao_baixar_imagem = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 160 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)
botao_salvar_edicoes = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 260 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)
botao_voltar_extra = pygame.Rect(DISTANCIA_DO_QUADRADO_DAS_IMAGENS_PARA_BOTOES, 360 + ALTURA_BOTOES, LARGURA_BOTOES, ALTURA_BOTOES)

lista_botoes_mais = [botao_salvar_caminho_pasta, botao_limpar_caminho_pasta, botao_baixar_imagem, botao_salvar_edicoes, botao_voltar_extra]