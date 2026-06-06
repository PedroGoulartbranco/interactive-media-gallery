import os
import sys
from random import choice, shuffle
import tkinter
from tkinter import filedialog

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
