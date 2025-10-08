
import customtkinter as ctk
from models import User
from .utils import carregar_usuarios, salvar_usuarios, tocar_som, SOM_ACERTO

class JanelaCadastro(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Cadastro de Usuário")
        self.geometry("400x500")
        self.transient(master)
        self.after(10, self.grab_set)

        self.setup_widgets()

    def setup_widgets(self):
        """Cria e posiciona os widgets na janela de cadastro."""
        ctk.CTkLabel(self, text="Cadastro", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(self, text="Usuário:").pack(pady=5)
        self.entry_novo_usuario = ctk.CTkEntry(self, placeholder_text="Mínimo 3 caracteres", width=250)
        self.entry_novo_usuario.pack(pady=5)
        
        ctk.CTkLabel(self, text="Senha:").pack(pady=5)
        self.entry_nova_senha = ctk.CTkEntry(self, placeholder_text="Mínimo 4 caracteres", show="*", width=250)
        self.entry_nova_senha.pack(pady=5)
        
        ctk.CTkLabel(self, text="Confirmar Senha:").pack(pady=5)
        self.entry_confirmar_senha = ctk.CTkEntry(self, placeholder_text="Confirme sua senha", show="*", width=250)
        self.entry_confirmar_senha.pack(pady=5)
        
        ctk.CTkLabel(self, text="Email (opcional):").pack(pady=5)
        self.entry_email = ctk.CTkEntry(self, placeholder_text="seu@email.com", width=250)
        self.entry_email.pack(pady=5)
        
        self.label_mensagem = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.label_mensagem.pack(pady=10)
        
        ctk.CTkButton(self, text="Cadastrar", command=self.realizar_cadastro, width=200).pack(pady=20)
        ctk.CTkButton(self, text="Cancelar", command=self.destroy, width=200, fg_color="gray").pack(pady=5)


    def realizar_cadastro(self):
        """Valida os dados e realiza o cadastro do novo usuário."""
        usuario = self.entry_novo_usuario.get().strip()
        senha = self.entry_nova_senha.get()
        confirmar = self.entry_confirmar_senha.get()
        email = self.entry_email.get().strip()

        # As validações continuam as mesmas...
        if not usuario or not senha:
            self.label_mensagem.configure(text="Usuário e senha são obrigatórios!", text_color="red")
            return
        # ... (outras validações) ...
        if senha != confirmar:
            self.label_mensagem.configure(text="As senhas não coincidem!", text_color="red")
            return

        usuarios = carregar_usuarios()

        if usuario in usuarios:
            self.label_mensagem.configure(text="Usuário já existe! Escolha outro.", text_color="red")
            return

        # --- ALTERAÇÃO PRINCIPAL AQUI ---
        # 1. Crie uma instância da classe User
        novo_usuario = User(nome=usuario, senha=senha, email=email)
        
        # 2. Salve o dicionário gerado pelo método to_dict()
        usuarios[usuario] = novo_usuario.to_dict()
        salvar_usuarios(usuarios)
        # --- FIM DA ALTERAÇÃO ---
        
        self.label_mensagem.configure(text="Cadastro realizado com sucesso!", text_color="green")
        tocar_som(SOM_ACERTO, volume=0.2)
        
        self.after(1500, self.destroy)