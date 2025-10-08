import os
import yaml
import pygame
from dotenv import load_dotenv

load_dotenv()
pygame.mixer.init()

SOM_ERRO = os.getenv("SOM_ERRO")
SOM_ACERTO = os.getenv("SOM_ACERTO")
ARQUIVO_USUARIOS = "usuarios.yaml"
IMAGEM_FUNDO_PATH = os.getenv("IMAGEM_FUNDO")


def tocar_som(caminho, volume=0.3):
    try:
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Erro ao tocar o som {caminho}: {e}")

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as file:
            usuarios = yaml.safe_load(file)
            return usuarios if usuarios else {}
    return {}

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as file:
        yaml.dump(usuarios, file, allow_unicode=True)