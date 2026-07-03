import PyInstaller.__main__
import os

nome = "Galeria"

argumentos = [
    'main.py',                               
    '--onefile',                            
    '--noconsole',                           
    f'--name={nome}',                
    f'--icon=imagens/galeria_icon.ico',     

    '--add-data=imagens;imagens/',
    '--add-data=sons;sons/',
    '--add-data=musicas;musicas/',
]

print(f"Iniciando a compilação de {nome}...")

PyInstaller.__main__.run(argumentos)

print("\nCompilação concluída com sucesso! Verifique a pasta 'dist'.")