# Login.py

import customtkinter as ctk
from PIL import Image, ImageOps, ImageEnhance
import os
from .cadastro import JanelaCadastro
from models import User
from .utils import (
    tocar_som, 
    carregar_usuarios, 
    SOM_ACERTO, 
    SOM_ERRO, 
    IMAGEM_FUNDO_PATH
)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bem-vindo ao Arcsound")
        self.geometry("350x450")
        self.resizable(False, False)

        self.setup_imagem_fundo()
        self.setup_widgets()

    def setup_imagem_fundo(self):
        if not IMAGEM_FUNDO_PATH or not os.path.exists(IMAGEM_FUNDO_PATH):
            raise FileNotFoundError("IMAGEM_FUNDO não definida no .env ou arquivo não existe.")

        self.imagem_fundo_original = Image.open(IMAGEM_FUNDO_PATH).resize((350, 450))
        self.imagem_fundo_dark = self._aplicar_opacidade(self.imagem_fundo_original.copy(), 0.3)
        
        img_invertida = ImageOps.invert(self.imagem_fundo_original.convert("RGB"))
        self.imagem_fundo_light = self._aplicar_opacidade(img_invertida, 0.3)
        
        self.label_fundo = ctk.CTkLabel(self, text="")
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        self.atualizar_fundo()

    def setup_widgets(self):
        ctk.CTkLabel(self, text="Arcsound", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=12, padx=10)

        self.botao_tema = ctk.CTkButton(self, text="☀", width=32, height=32, command=self.alternar_tema)
        self.botao_tema.place(relx=1.0, x=-10, y=10, anchor="ne")

        ctk.CTkLabel(self, text="Usuário:").pack(pady=10)
        self.insere_usuario = ctk.CTkEntry(self, placeholder_text="Insira seu usuário")
        self.insere_usuario.pack(pady=10)

        ctk.CTkLabel(self, text="Senha:").pack(pady=10)
        
        senha_frame = ctk.CTkFrame(self)
        senha_frame.pack(pady=10)

        self.insere_senha = ctk.CTkEntry(senha_frame, placeholder_text="Insira sua senha", show="*")
        self.insere_senha.pack(side="left", padx=(0, 5))
        self.botao_mostrar_senha = ctk.CTkButton(senha_frame, text="Mostrar", command=self.alternar_senha, width=80)
        self.botao_mostrar_senha.pack(side="left")

        ctk.CTkButton(self, text="Login", command=self.validar_login).pack(pady=10)
        ctk.CTkButton(self, text="Cadastrar-se", command=self.abrir_cadastro, fg_color="gray", hover_color="darkgray").pack(pady=5)
        
        self.login_sucesso = ctk.CTkLabel(self, text='')
        self.login_sucesso.pack(pady=10)

    def validar_login(self):
        """Verifica as credenciais do usuário."""
        usuario = self.insere_usuario.get()
        senha = self.insere_senha.get()
        usuarios = carregar_usuarios()
        
        # A lógica de verificação continua funcionando
        if usuario in usuarios and usuarios[usuario]['senha'] == senha:
            self.login_sucesso.configure(text="Login realizado com sucesso!", text_color="green")
            tocar_som(SOM_ACERTO, volume=0.2)

            # ✨ Opcional, mas recomendado:
            # Carregue os dados do usuário em um objeto após o login
            dados_usuario = usuarios[usuario]
            usuario_logado = User.from_dict(dados_usuario)
            
            print("Usuário logado:", usuario_logado) # Exibe o objeto no console
            # Agora você pode passar o objeto 'usuario_logado' para outras partes do seu app

        else:
            self.login_sucesso.configure(text="Usuário ou senha incorretos.", text_color="red")
            tocar_som(SOM_ERRO, volume=0.2)

    def abrir_cadastro(self):
        """Abre a janela de cadastro."""
        JanelaCadastro(self)

    def alternar_senha(self):
        """Alterna a visibilidade da senha no campo de entrada."""
        if self.insere_senha.cget("show") == "*":
            self.insere_senha.configure(show="")
            self.botao_mostrar_senha.configure(text="Ocultar")
        else:
            self.insere_senha.configure(show="*")
            self.botao_mostrar_senha.configure(text="Mostrar")

    def _aplicar_opacidade(self, img, opacidade):
        """Aplica um nível de opacidade a uma imagem."""
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        alpha = img.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacidade)
        img.putalpha(alpha)
        return img

    def atualizar_fundo(self):
        """Atualiza a imagem de fundo com base no tema atual."""
        modo_atual = ctk.get_appearance_mode()
        img = self.imagem_fundo_dark if modo_atual == "Dark" else self.imagem_fundo_light
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(350, 450))
        self.label_fundo.configure(image=img_ctk)

    def alternar_tema(self):
        """Alterna entre os temas claro e escuro."""
        modo_atual = ctk.get_appearance_mode()
        if modo_atual == "Dark":
            ctk.set_appearance_mode("light")
            self.botao_tema.configure(text="☾")
        else:
            ctk.set_appearance_mode("dark")
            self.botao_tema.configure(text="☀")
        self.atualizar_fundo()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()