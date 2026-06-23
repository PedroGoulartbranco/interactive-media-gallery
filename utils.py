import os
import sys
from random import choice, shuffle
import tkinter
from tkinter import filedialog, Tk
import json
import pygame
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops, ImageDraw

lista_musicas = [
    {"nome": "So Easy to Fall in Love","caminho": "sons\olivia_dean___so_easy__to_fall_in_love___lyrics_.mp3"},
    {"nome": "For Youth","caminho": "sons\o___for_youth__legendado_tradu__o_.mp3"}
]

def listar_fotos(caminho):
    lista = []
    extensoes_foto = (".png", ".jpg", ".jpeg")
    
    for arquivo in os.listdir(caminho):
        if arquivo.lower().endswith(extensoes_foto):
            caminho_completo = os.path.join(caminho, arquivo)
            lista.append(caminho_completo)
            
    lista.sort()
    
    return len(lista), lista

def caminho_recurso(rel_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

def aleatorizar(numero_fotos, indice_foto_atual):
    fotos_opcoes = []
    for indice_foto in range(numero_fotos):
        if indice_foto != indice_foto_atual:
            fotos_opcoes.append(indice_foto)
    return choice(fotos_opcoes)

def musica_atual(indice):
    return lista_musicas[indice]["nome"], caminho_recurso(lista_musicas[indice]["caminho"])

def abrir_pasta():
    root = tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    caminho = filedialog.askdirectory()
    
    root.destroy()
    
    return caminho


def verificar_pasta(caminho):
    if os.path.isdir(caminho):
        return True
    return False

def tocar_musica(indice):
    nome_musica_atual, caminho_musica_atual = musica_atual(indice)

    return nome_musica_atual, caminho_musica_atual

def embaralhar_fotos(lista_fotos):
    return shuffle(lista_fotos)

def salvar_caminho_json(caminho):
    caminho_json = caminho_recurso("configuracoes.json")
    dados = {}
    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    dados["caminho"] = caminho

    with open(caminho_json, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

def limpar_caminho_json():
    caminho_json = caminho_recurso("configuracoes.json")
    dados = {}

    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    dados["caminho"] = ""

    with open(caminho_json, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

def pegar_configuracoes_salvas():
    caminho_json = caminho_recurso("configuracoes.json")
    dados = {}

    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return dados

def salvar_configuracoes_json(cor_fundo, cor_botoes, cor_borda):
    caminho_json = caminho_recurso("configuracoes.json")
    dados = {}

    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    dados["cor_fundo"] = cor_fundo
    dados["cor_botoes"] = cor_botoes
    dados["cor_borda"] = cor_borda

    with open(caminho_json, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    return dados

def baixar_imagem(imagem):
    imagem_pillow = pygame_para_pillow(imagem)

    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True) # Força a janela de salvar a ficar na frente de tudo

    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Imagem PNG", "*.png")],
        title="Escolha onde salvar sua imagem"
    )

    if caminho_arquivo:
        imagem_pillow.save(caminho_arquivo, format="PNG")

def pygame_para_pillow(surface):
    modo = "RGBA" if surface.get_alpha() else "RGB"

    dados = pygame.image.tobytes(surface, modo)

    imagem_pil = Image.frombytes(
        modo,
        surface.get_size(),
        dados
    )

    return imagem_pil