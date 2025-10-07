import customtkinter as ctk
from playsound import playsound
from PIL import Image, ImageOps, ImageEnhance
import pygame

pygame.mixer.init()

som_erro = r"c:\Users\bernardo portalet\Downloads\necoarc-nyanyanya.mp3"
som_acerto = r"c:\Users\bernardo portalet\Downloads\Neco-Arc sound effect - les mashav (youtube).mp3"

def tocar_som(caminho, volume=0.3):
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

#esquci de fazer o validar login ai preciso botar outras variaveis
#e acabei tendo que trocar a variavel usuario por top_usuario
#pra mostrar que é um label
def validar_login():
    usuario = insere_usuario.get()
    senha = insere_senha.get()

    if usuario == "arthur" and senha == "1234":
        login_sucesso.configure(text="Login realizado com sucesso!", text_color="green")
        tocar_som(som_acerto, volume=0.2)
    else:
        login_sucesso.configure(text="Usuário ou senha incorretos.", text_color="red")
        tocar_som(som_erro, volume=0.2)

def alternar_senha():
    if insere_senha.cget("show") == "*":
        insere_senha.configure(show="")
        botao_mostrar_senha.configure(text="Ocultar Senha")
    else:
        insere_senha.configure(show="*")
        botao_mostrar_senha.configure(text="Mostrar Senha")

def aplicar_opacidade(img, opacidade):
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    alpha = img.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacidade)
    img.putalpha(alpha)
    return img

imagem_fundo = Image.open(r"c:\Users\bernardo portalet\Downloads\necoarcteste-removebg-preview.png").resize((350,450))
imagem_fundo = aplicar_opacidade(imagem_fundo, 0.3)

def atualizar_fundo():
    modo_atual = ctk.get_appearance_mode()
    if modo_atual == "Dark":
        img = imagem_fundo
    else: 
        img = ImageOps.invert(imagem_fundo.convert("RGB"))
        img = aplicar_opacidade(img, 0.3)
    img_ctk = ctk.CTkImage(img, size=(350,450))
    label_fundo.configure(image=img_ctk)
    label_fundo.image = img_ctk

def alternar_tema():
    modo_atual = ctk.get_appearance_mode() 
    if modo_atual == "Dark":
        ctk.set_appearance_mode("light")
        botao_tema.configure(text="☾")
    else:
        ctk.set_appearance_mode("dark")
        botao_tema.configure(text="☀")

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Bem-vindo ao Arcsound")
app.geometry("350x450")

# Adicione o label de fundo ANTES dos outros widgets
img_ctk = ctk.CTkImage(imagem_fundo, size=(350, 450))
label_fundo = ctk.CTkLabel(app, image=img_ctk, text="")
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

ctk.CTkLabel(app, text="Arcsound", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=12, padx=10)

botao_tema = ctk.CTkButton(app, text="☀", width=32, height=32, command=alternar_tema)
botao_tema.place(relx=1.0,x= -10, y=10, anchor="ne")

#adicionar usuario
top_usuario = ctk.CTkLabel(app, text = "Usuário:")
top_usuario.pack(pady=10)

insere_usuario = ctk.CTkEntry(app,placeholder_text="Insira seu usuário")
insere_usuario.pack(pady=10)

#adicionar senha 
top_senha = ctk.CTkLabel(app, text = "Senha:")
top_senha.pack(pady=10)


senha_frame = ctk.CTkFrame(app)
senha_frame.pack(pady=10)

insere_senha = ctk.CTkEntry(senha_frame, placeholder_text="Insira sua senha", show="*")
insere_senha.pack(side="left", padx=(0, 5))

botao_mostrar_senha = ctk.CTkButton(senha_frame, text="Mostrar Senha", command=alternar_senha, width=120)
botao_mostrar_senha.pack(side="left")

#insere_senha = ctk.CTkEntry(app,placeholder_text="Insira sua senha", show = "*")
#insere_senha.pack(pady=10)
#botao_mostrar_senha = ctk.CTkButton(app, text="Mostrar Senha", command=alternar_senha) 
#botao_mostrar_senha.pack(pady=5)

botao_login = ctk.CTkButton(app, text="Login", command= validar_login)
botao_login.pack(pady = 10)

#caso aconteça o login
login_sucesso = ctk.CTkLabel(app,text='') 
login_sucesso.pack(pady=10)

atualizar_fundo()

app.mainloop()
