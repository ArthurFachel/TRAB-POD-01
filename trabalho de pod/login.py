import customtkinter as ctk
from playsound import playsound
from PIL import Image, ImageOps, ImageEnhance
import pygame
import yaml
import os

pygame.mixer.init()

som_erro = r"c:\Users\bernardo portalet\Downloads\necoarc-nyanyanya.mp3"
som_acerto = r"c:\Users\bernardo portalet\Downloads\Neco-Arc sound effect - les mashav (youtube).mp3"
arquivo_usuarios = "usuarios.yaml"

def tocar_som(caminho, volume=0.3):
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

def carregar_usuarios():
    """Carrega os usuários do arquivo YAML"""
    if os.path.exists(arquivo_usuarios):
        with open(arquivo_usuarios, 'r', encoding='utf-8') as file:
            usuarios = yaml.safe_load(file)
            return usuarios if usuarios else {}
    return {}

def salvar_usuarios(usuarios):
    """Salva os usuários no arquivo YAML"""
    with open(arquivo_usuarios, 'w', encoding='utf-8') as file:
        yaml.dump(usuarios, file, allow_unicode=True)

def validar_login():
    usuario = insere_usuario.get()
    senha = insere_senha.get()
    
    usuarios = carregar_usuarios()
    
    if usuario in usuarios and usuarios[usuario]['senha'] == senha:
        login_sucesso.configure(text="Login realizado com sucesso!", text_color="green")
        tocar_som(som_acerto, volume=0.2)
    else:
        login_sucesso.configure(text="Usuário ou senha incorretos.", text_color="red")
        tocar_som(som_erro, volume=0.2)

def abrir_cadastro():
    """Abre a janela de cadastro"""
    janela_cadastro = ctk.CTkToplevel(app)
    janela_cadastro.title("Cadastro de Usuário")
    janela_cadastro.geometry("400x500")
    janela_cadastro.grab_set()  # Torna a janela modal
    
    # Título
    ctk.CTkLabel(janela_cadastro, text="Cadastro", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
    
    # Campo Usuário
    ctk.CTkLabel(janela_cadastro, text="Usuário:").pack(pady=5)
    entry_novo_usuario = ctk.CTkEntry(janela_cadastro, placeholder_text="Escolha um nome de usuário", width=250)
    entry_novo_usuario.pack(pady=5)
    
    # Campo Senha
    ctk.CTkLabel(janela_cadastro, text="Senha:").pack(pady=5)
    entry_nova_senha = ctk.CTkEntry(janela_cadastro, placeholder_text="Escolha uma senha", show="*", width=250)
    entry_nova_senha.pack(pady=5)
    
    # Campo Confirmar Senha
    ctk.CTkLabel(janela_cadastro, text="Confirmar Senha:").pack(pady=5)
    entry_confirmar_senha = ctk.CTkEntry(janela_cadastro, placeholder_text="Confirme sua senha", show="*", width=250)
    entry_confirmar_senha.pack(pady=5)
    
    # Campo Email (opcional)
    ctk.CTkLabel(janela_cadastro, text="Email (opcional):").pack(pady=5)
    entry_email = ctk.CTkEntry(janela_cadastro, placeholder_text="seu@email.com", width=250)
    entry_email.pack(pady=5)
    
    # Label de mensagem
    label_mensagem = ctk.CTkLabel(janela_cadastro, text="", font=ctk.CTkFont(size=12))
    label_mensagem.pack(pady=10)
    
    def realizar_cadastro():
        """Realiza o cadastro do novo usuário"""
        usuario = entry_novo_usuario.get().strip()
        senha = entry_nova_senha.get()
        confirmar = entry_confirmar_senha.get()
        email = entry_email.get().strip()
        
        # Validações
        if not usuario or not senha:
            label_mensagem.configure(text="Usuário e senha são obrigatórios!", text_color="red")
            return
        
        if len(usuario) < 3:
            label_mensagem.configure(text="Usuário deve ter no mínimo 3 caracteres!", text_color="red")
            return
        
        if len(senha) < 4:
            label_mensagem.configure(text="Senha deve ter no mínimo 4 caracteres!", text_color="red")
            return
        
        if senha != confirmar:
            label_mensagem.configure(text="As senhas não coincidem!", text_color="red")
            return
        
        # Carregar usuários existentes
        usuarios = carregar_usuarios()
        
        # Verificar se usuário já existe
        if usuario in usuarios:
            label_mensagem.configure(text="Usuário já existe! Escolha outro.", text_color="red")
            return
        
        # Adicionar novo usuário
        usuarios[usuario] = {
            'senha': senha,
            'email': email if email else None
        }
        
        # Salvar no arquivo
        salvar_usuarios(usuarios)
        
        label_mensagem.configure(text="Cadastro realizado com sucesso!", text_color="green")
        tocar_som(som_acerto, volume=0.2)
        
        # Fechar janela após 1.5 segundos
        janela_cadastro.after(1500, janela_cadastro.destroy)
    
    # Botão Cadastrar
    ctk.CTkButton(janela_cadastro, text="Cadastrar", command=realizar_cadastro, width=200).pack(pady=20)
    
    # Botão Cancelar
    ctk.CTkButton(janela_cadastro, text="Cancelar", command=janela_cadastro.destroy, width=200, fg_color="gray").pack(pady=5)

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

# Label de fundo
img_ctk = ctk.CTkImage(imagem_fundo, size=(350, 450))
label_fundo = ctk.CTkLabel(app, image=img_ctk, text="")
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

ctk.CTkLabel(app, text="Arcsound", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=12, padx=10)

botao_tema = ctk.CTkButton(app, text="☀", width=32, height=32, command=alternar_tema)
botao_tema.place(relx=1.0, x=-10, y=10, anchor="ne")

# Campo usuário
top_usuario = ctk.CTkLabel(app, text="Usuário:")
top_usuario.pack(pady=10)

insere_usuario = ctk.CTkEntry(app, placeholder_text="Insira seu usuário")
insere_usuario.pack(pady=10)

# Campo senha
top_senha = ctk.CTkLabel(app, text="Senha:")
top_senha.pack(pady=10)

senha_frame = ctk.CTkFrame(app)
senha_frame.pack(pady=10)

insere_senha = ctk.CTkEntry(senha_frame, placeholder_text="Insira sua senha", show="*")
insere_senha.pack(side="left", padx=(0, 5))

botao_mostrar_senha = ctk.CTkButton(senha_frame, text="Mostrar Senha", command=alternar_senha, width=120)
botao_mostrar_senha.pack(side="left")

# Botão de Login
botao_login = ctk.CTkButton(app, text="Login", command=validar_login)
botao_login.pack(pady=10)

# Botão de Cadastro (NOVO)
botao_cadastro = ctk.CTkButton(app, text="Cadastrar-se", command=abrir_cadastro, fg_color="gray", hover_color="darkgray")
botao_cadastro.pack(pady=5)

# Label de mensagem de login
login_sucesso = ctk.CTkLabel(app, text='') 
login_sucesso.pack(pady=10)

atualizar_fundo()

app.mainloop()

