import os
import sys

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