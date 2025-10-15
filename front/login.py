from tkinter import filedialog
import json
import os
import yaml
import customtkinter as ctk
from PIL import Image, ImageEnhance, ImageOps
import pygame
from models.getfile import parse_data_file
from .player import PlayerMusica

#Boa sorte pra quem tentar entender esse código
#Horas gastas tentando arrumar o ADMIN panel: 12



pygame.mixer.init()

SOM_ERRO = r"c:\Users\bernardo portalet\Downloads\necoarc-nyanyanya.mp3"
SOM_ACERTO = r"c:\Users\bernardo portalet\Downloads\Neco-Arc sound effect - les mashav (youtube).mp3"
ARQUIVO_USUARIOS = "usuarios.yaml"
IMAGEM_FUNDO_PATH = r"c:\Users\bernardo portalet\Downloads\necoarcteste-removebg-preview.png"


def tocar_som(caminho: str, volume: float = 0.3) -> None:
    try:
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
    except Exception:
        pass


def carregar_usuarios() -> dict:
    """
    Lê usuarios.yaml e normaliza a estrutura para um dict:
    { username: { 'nome': username, 'senha': ..., 'email': ..., 'historico': [], 'playlists': [], 'biblioteca': [] } }
    Aceita entradas antigas como listas ou arquivos com lista de objetos e faz migração em memória.
    """
    if not os.path.exists(ARQUIVO_USUARIOS):
        return {}

    with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as file:
        raw = yaml.safe_load(file)

    if not raw:
        return {}

    # Se veio uma lista (ex.: [{nome: 'arthur', ...}, {...}]) -> transformar em dict
    if isinstance(raw, list):
        normalized = {}
        for entry in raw:
            if isinstance(entry, dict):
                key = entry.get("nome") or entry.get("username") or entry.get("user") or None
                if not key:
                    # usa índice como fallback
                    key = f"usuario_{len(normalized)+1}"
                normalized[key] = entry
            else:
                continue
        raw = normalized

    usuarios_norm = {}
    for key, val in raw.items():
        if isinstance(val, list):
            usuarios_norm[key] = {
                "nome": key,
                "senha": None,
                "email": None,
                "historico": [],
                "playlists": val,
                "biblioteca": [],
            }
            continue

        if not isinstance(val, dict):
            # valor estranho -> pular
            continue

        u = dict(val) 
        # preencher chaves faltantes
        u.setdefault("nome", key)
        u.setdefault("senha", None)
        u.setdefault("email", None)
        u.setdefault("historico", [])
        u.setdefault("playlists", [])
        u.setdefault("biblioteca", [])
        usuarios_norm[key] = u

    return usuarios_norm



def salvar_usuarios(usuarios: dict) -> None:
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as file:
        yaml.dump(usuarios, file, allow_unicode=True)


class JanelaCadastro(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Usuário")
        self.geometry("400x500")
        self.transient(master)
        self.after(10, self.grab_set)
        self.setup_widgets()

    def setup_widgets(self) -> None:
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

    def realizar_cadastro(self) -> None:
        usuario = self.entry_novo_usuario.get().strip()
        senha = self.entry_nova_senha.get()
        confirmar = self.entry_confirmar_senha.get()
        email = self.entry_email.get().strip()

        if not usuario or not senha:
            self.label_mensagem.configure(text="Usuário e senha são obrigatórios!", text_color="red")
            return

        if len(usuario) < 3:
            self.label_mensagem.configure(text="Usuário deve ter no mínimo 3 caracteres!", text_color="red")
            return

        if len(senha) < 4:
            self.label_mensagem.configure(text="Senha deve ter no mínimo 4 caracteres!", text_color="red")
            return

        if senha != confirmar:
            self.label_mensagem.configure(text="As senhas não coincidem!", text_color="red")
            return

        usuarios = carregar_usuarios()
        if usuario in usuarios:
            self.label_mensagem.configure(text="Usuário já existe! Escolha outro.", text_color="red")
            return

        usuarios[usuario] = {
            "nome": usuario,
            "senha": senha,
            "email": email if email else None,
            "historico": [],
            "playlists": [],
        }

        salvar_usuarios(usuarios)
        self.label_mensagem.configure(text="Cadastro realizado com sucesso!", text_color="green")
        tocar_som(SOM_ACERTO, volume=0.2)
        self.after(1500, self.destroy)


class AdminPage(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Admin Panel")
        self.geometry("600x400")
        self.transient(master)
        self.setup_widgets()

    def setup_widgets(self) -> None:
        ctk.CTkLabel(self, text="Admin Panel", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=(0,10))

        self.drop_frame = ctk.CTkFrame(self, width=400, height=200)
        self.drop_frame.pack(pady=20, padx=20)
        ctk.CTkLabel(self.drop_frame, text="Arquivo markdown aqui \nor").pack(pady=(20, 5))
        ctk.CTkButton(self.drop_frame, text="Browse Files", command=self.browse_file).pack(pady=5)

        self.results_text = ctk.CTkTextbox(self, width=400, height=200)
        self.results_text.pack(pady=20, padx=20)

    def browse_file(self) -> None:
        file_path = filedialog.askopenfilename(title="Select MD File", filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
        if file_path:
            self.process_md_file(file_path)

    def process_md_file(self, file_path: str) -> None:
        try:
            sections = parse_data_file(file_path) or []
            usuarios = carregar_usuarios()

            users_section = []
            musics_section = []
            playlists_section = []

            for sec in sections:
                if not isinstance(sec, list):
                    continue
                for item in sec:
                    if not isinstance(item, dict):
                        continue
                    if "titulo" in item and ("artista" in item or "duracao" in item or "genero" in item):
                        musics_section.append(item)
                    elif "titulo" in item and ("episodio" in item or "temporada" in item or "host" in item):
                        musics_section.append(item)
                    elif "itens" in item or "usuario" in item or "musicas" in item or "tracks" in item:
                        playlists_section.append(item)
                    elif "nome" in item:
                        users_section.append(item)

            def ensure_user(username: str) -> dict:
                if username not in usuarios:
                    usuarios[username] = {
                        "nome": username,
                        "senha": "default123",
                        "email": None,
                        "historico": [],
                        "playlists": [],
                        "biblioteca": [],
                    }
                else:
                    usuarios[username].setdefault("biblioteca", [])
                    usuarios[username].setdefault("playlists", [])
                    usuarios[username].setdefault("historico", [])
                return usuarios[username]

            def normalize_title(item) -> str:
                if isinstance(item, dict):
                    title = item.get("titulo") or item.get("nome") or item.get("arquivo") or ""
                else:
                    title = str(item).strip()
                if not title:
                    return ""
                base = os.path.basename(title)
                name, _ = os.path.splitext(base)
                return name or title

            for u in users_section:
                ensure_user(u["nome"])

            for m in musics_section:
                titulo = normalize_title(m)
                if not titulo:
                    continue

            for p in playlists_section:
                owner = p.get("usuario") or p.get("autor") or p.get("criador")
                name = p.get("nome") or p.get("titulo")
                itens = p.get("itens") or p.get("musicas") or p.get("tracks") or []
                if not name:
                    continue
                if not owner:
                    owner = p.get("usuario") or None
                if owner:
                    user = ensure_user(owner)
                else:
                    # sem : cria/usa um usuário genérico "Unknown"
                    user = ensure_user("Unknown")

                titulos = []
                for item in itens:
                    title_text = normalize_title(item)
                    if not title_text:
                        continue
                    titulos.append(title_text)
                    if title_text not in user["biblioteca"]:
                        user["biblioteca"].append(title_text)

                if not any(pl.get("nome") == name for pl in user["playlists"]):
                    user["playlists"].append({"nome": name, "musicas": titulos})

            for u in users_section:
                username = u.get("nome")
                if not username:
                    continue
                user = ensure_user(username)
                if "playlists" in u:
                    for plref in u["playlists"]:
                        pl_name = None
                        itens = []
                        if isinstance(plref, dict):
                            pl_name = plref.get("nome") or plref.get("titulo")
                            itens = plref.get("itens") or plref.get("musicas") or []
                        else:
                            pl_name = str(plref)
                            # tenta achar dados completos na playlists_section
                            pl_obj = next((pp for pp in playlists_section if (pp.get("nome") == pl_name and (pp.get("usuario") in (None, username)))), None)
                            if pl_obj:
                                itens = pl_obj.get("itens") or pl_obj.get("musicas") or []

                        if not pl_name:
                            continue
                        titulos = []
                        for item in itens:
                            title_text = normalize_title(item)
                            if not title_text:
                                continue
                            titulos.append(title_text)
                            if title_text not in user["biblioteca"]:
                                user["biblioteca"].append(title_text)
                        if not any(pl.get("nome") == pl_name for pl in user["playlists"]):
                            user["playlists"].append({"nome": pl_name, "musicas": titulos})

            salvar_usuarios(usuarios)

            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"Processed file: {file_path}\n\n")
            self.results_text.insert("end", f"Usuários no arquivo: {len(users_section)}\n")
            self.results_text.insert("end", f"Playlists detectadas: {len(playlists_section)}\n")
            self.results_text.insert("end", f"Músicas detectadas: {len(musics_section)}\n\n")

            for u in users_section:
                nome = u.get("nome")
                user = usuarios.get(nome, {})
                self.results_text.insert("end", f"- {nome}\n")
                self.results_text.insert("end", f"  Playlists: {len(user.get('playlists', []))}\n")
                bib = user.get("biblioteca", [])
                if bib:
                    self.results_text.insert("end", f"  Biblioteca (text): {len(bib)} itens\n")
                    for t in bib:
                        self.results_text.insert("end", f"    - {t}\n")

            self.results_text.insert("end", "\nOpening Admin Player View...")
            self.after(1200, self.open_admin_player)

        except Exception as e:
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"Error processing file:\n{str(e)}")

    def open_admin_player(self) -> None:
        AdminPlayerView(self.master)
        self.destroy()

    def _on_admin_select(self, val: str) -> None:
        if val == "adm":
            from models.admin import (
                top_musicas_reproduzidas,
                playlist_mais_popular,
                usuario_mais_ativo,
                media_avaliacoes,
                total_reproducoes,
            )
            ReportWindow(self, top_musicas_reproduzidas, playlist_mais_popular, usuario_mais_ativo, media_avaliacoes, total_reproducoes)


class ReportWindow(ctk.CTkToplevel):
    def __init__(self, master, fn_top, fn_playlist_pop, fn_usuario_ativo, fn_media, fn_total):
        super().__init__(master)
        self.title("Relatórios - Admin")
        self.geometry("700x520")
        self.transient(master)
        self.fn_top = fn_top
        self.fn_playlist_pop = fn_playlist_pop
        self.fn_usuario_ativo = fn_usuario_ativo
        self.fn_media = fn_media
        self.fn_total = fn_total
        self.setup_ui()

    def setup_ui(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        btns = ctk.CTkFrame(frame)
        btns.pack(fill="x", pady=(0,8))

        ctk.CTkButton(btns, text="Top Músicas (Top 10)", command=self._show_top).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Playlist Mais Popular", command=self._show_playlist_pop).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Usuário Mais Ativo", command=self._show_usuario_ativo).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Média Avaliações", command=self._show_media).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Total Reproduções", command=self._show_total).pack(side="left", padx=6)

        self.output = ctk.CTkTextbox(frame, width=660, height=420)
        self.output.pack(fill="both", expand=True, pady=(8,0))

    def _show_top(self):
        self.output.delete("1.0", "end")
        try:
            items = self.fn_top(10)
            if not items:
                self.output.insert("1.0", "Nenhuma reprodução registrada.\n")
                return
            self.output.insert("1.0", "Top Músicas Mais Reproduzidas:\n\n")
            for i, it in enumerate(items, 1):
                titulo = it.get("titulo") or str(it)
                reproducoes = it.get("reproducoes", 0)
                self.output.insert("end", f"{i}. {titulo} — {reproducoes} reproduções\n")
        except Exception as e:
            self.output.insert("1.0", f"Erro: {e}\n")

    def _show_playlist_pop(self):
        self.output.delete("1.0", "end")
        try:
            pl = self.fn_playlist_pop()
            if not pl:
                self.output.insert("1.0", "Nenhuma playlist encontrada.\n")
                return
            self.output.insert("1.0", f"Playlist Mais Popular:\n\nNome: {pl.get('nome')}\nUsuário: {pl.get('usuario')}\nReproduções: {pl.get('reproducoes')}\nMúsicas:\n")
            for m in pl.get("musicas", []):
                self.output.insert("end", f"  - {m}\n")
        except Exception as e:
            self.output.insert("1.0", f"Erro: {e}\n")

    def _show_usuario_ativo(self):
        self.output.delete("1.0", "end")
        try:
            u = self.fn_usuario_ativo()
            if not u:
                self.output.insert("1.0", "Nenhum usuário encontrado.\n")
                return
            self.output.insert("1.0", f"Usuário Mais Ativo: {u.get('nome')}\nTotal reproduções: {u.get('total_reproducoes')}\n")
        except Exception as e:
            self.output.insert("1.0", f"Erro: {e}\n")

    def _show_media(self):
        self.output.delete("1.0", "end")
        try:
            medias = self.fn_media()
            if not medias:
                self.output.insert("1.0", "Nenhuma avaliação registrada.\n")
                return
            self.output.insert("1.0", "Média de Avaliações por Música:\n\n")
            for titulo, m in medias.items():
                self.output.insert("end", f"{titulo}: {m:.2f}\n")
        except Exception as e:
            self.output.insert("1.0", f"Erro: {e}\n")

    def _show_total(self):
        self.output.delete("1.0", "end")
        try:
            total = self.fn_total()
            self.output.insert("1.0", f"Total de reproduções (todos usuários): {total}\n")
        except Exception as e:
            self.output.insert("1.0", f"Erro: {e}\n")


class AdminPlayerView(PlayerMusica):
    def __init__(self, master):
        admin_user = {"nome": "Admin", "senha": "admin", "email": None, "historico": [], "playlists": []}
        super().__init__(master=master, usuario_logado=admin_user)
        self.title("Admin Player View")
        self.setup_admin_controls()

        usuarios = self.get_user_list()
        if usuarios:
            self.switch_user(usuarios[0])

    def setup_admin_controls(self) -> None:
        admin_frame = ctk.CTkFrame(self)
        admin_frame.pack(fill="x", padx=10, pady=5, before=self.winfo_children()[0])

        usuarios = self.get_user_list()
        # garantir que 'adm' sempre apareça no seletor
        valores = list(dict.fromkeys((usuarios or []) + ["adm"]))

        self.user_var = ctk.StringVar(value=valores[0] if valores else "No Users")
        self.users_dropdown = ctk.CTkOptionMenu(
            admin_frame,
            variable=self.user_var,
            values=valores,
            command=self._on_adminplayer_user_select,  
        )
        self.users_dropdown.pack(side="left", padx=5)

        ctk.CTkButton(admin_frame, text="Save Changes", command=self.save_changes, fg_color="green", hover_color="dark green").pack(side="right", padx=5)
        self.status_label = ctk.CTkLabel(admin_frame, text="")
        self.status_label.pack(side="left", padx=5)

    def _on_adminplayer_user_select(self, username: str) -> None:
        if not username:
            return

        if username == "adm":
            from models.admin import (
                top_musicas_reproduzidas,
                playlist_mais_popular,
                usuario_mais_ativo,
                media_avaliacoes,
                total_reproducoes,
            )
            ReportWindow(self, top_musicas_reproduzidas, playlist_mais_popular, usuario_mais_ativo, media_avaliacoes, total_reproducoes)
            try:
                self.user_var.set("adm")
            except Exception:
                pass
            return

        self.switch_user(username)

    def get_user_list(self) -> list:
        usuarios = carregar_usuarios()
        return list(usuarios.keys())

    def switch_user(self, username: str) -> None:
        usuarios = carregar_usuarios()
        if username not in usuarios:
            self.show_status(f"Usuário '{username}' não encontrado.", "red")
            return

        user = usuarios[username]

        if isinstance(user, list):
            user = {
                "nome": username,
                "senha": None,
                "email": None,
                "historico": [],
                "playlists": user,
                "biblioteca": [],
            }

        if not isinstance(user, dict):
            user = {
                "nome": username,
                "senha": None,
                "email": None,
                "historico": [],
                "playlists": [],
                "biblioteca": [],
            }

        user.setdefault("nome", username)
        user.setdefault("senha", None)
        user.setdefault("email", None)
        user.setdefault("historico", [])
        user.setdefault("playlists", [])
        user.setdefault("biblioteca", [])

        self.usuario_logado = user
        try:
            self.user_var.set(username)
        except Exception:
            pass

        self.atualizar_interface()
        try:
            self.carregar_dados_usuario()
        except Exception:
            pass


    def save_changes(self) -> None:
        """
        Salva alterações do usuário atual em usuarios.yaml e registra um log detalhado
        em 'changes.log' incluindo diferenças aplicadas (detecta mudanças em listas/dicts).
        """
        import datetime
        import traceback
        import copy
        import json

        log_path = "changes.log"

        try:
            if not getattr(self, "usuario_logado", None):
                msg = "Nenhum usuário carregado para salvar."
                with open(log_path, "a", encoding="utf-8") as lf:
                    lf.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] SAVE_ATTEMPT - no user loaded\n{msg}\n\n")
                self.show_status(msg, "red")
                return

            # carrega snapshot antes das mudanças
            usuarios_before = carregar_usuarios()
            snapshot_before = copy.deepcopy(usuarios_before)

            usuarios = usuarios_before
            key = self.usuario_logado.get("nome") or (self.user_var.get() if hasattr(self, "user_var") else None)
            if not key:
                existing_keys = list(usuarios.keys())
                key = existing_keys[0] if existing_keys else None

            if not key:
                raise RuntimeError("Nenhuma chave válida encontrada para salvar o usuário.")

            usuarios[key] = self.usuario_logado
            salvar_usuarios(usuarios)

            # recarrega arquivo salvo para comparação
            usuarios_after = carregar_usuarios()
            snapshot_after = copy.deepcopy(usuarios_after)

            def diff_dict(prev: dict, new: dict) -> list[str]:
                lines = []
                keys = set(prev.keys()) | set(new.keys())
                for k in sorted(keys):
                    a = prev.get(k, None)
                    b = new.get(k, None)
                    if a == b:
                        continue
                    if isinstance(a, list) and isinstance(b, list):
                        added = [i for i in b if i not in a]
                        removed = [i for i in a if i not in b]
                        if added:
                            lines.append(f"{k} +added: {json.dumps(added, ensure_ascii=False)}")
                        if removed:
                            lines.append(f"{k} -removed: {json.dumps(removed, ensure_ascii=False)}")
                    elif isinstance(a, dict) and isinstance(b, dict):
                        try:
                            if a != b:
                                lines.append(f"{k}: {json.dumps(a, ensure_ascii=False)} -> {json.dumps(b, ensure_ascii=False)}")
                        except Exception:
                            lines.append(f"{k}: changed")
                    else:
                        lines.append(f"{k}: {a!r} -> {b!r}")
                return lines

            changes = []

            # diffs do usuário específico
            prev_user = snapshot_before.get(key, {})
            new_user = snapshot_after.get(key, {})
            user_changes = diff_dict(prev_user, new_user)
            if user_changes:
                changes.append(f"User '{key}' changes:")
                changes.extend([f"  {ln}" for ln in user_changes])

            # diffs da BIBLIOTECA global (se existir)
            prev_lib = snapshot_before.get("BIBLIOTECA", [])
            new_lib = snapshot_after.get("BIBLIOTECA", [])
            if prev_lib != new_lib:
                added = [m for m in new_lib if m not in prev_lib]
                removed = [m for m in prev_lib if m not in new_lib]
                if added or removed:
                    changes.append("Global BIBLIOTECA changes:")
                    if added:
                        changes.append(f"  +added: {json.dumps(added, ensure_ascii=False)}")
                    if removed:
                        changes.append(f"  -removed: {json.dumps(removed, ensure_ascii=False)}")

            if not changes:
                changes = ["Nenhuma alteração detectada (salvamento forçado)."]

            # grava log legível
            ui_status = ""
            try:
                if hasattr(self, "status_label") and getattr(self.status_label, "cget", None):
                    ui_status = self.status_label.cget("text") or ""
            except Exception:
                ui_status = ""

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_path, "a", encoding="utf-8") as lf:
                lf.write(f"[{timestamp}] SAVE_CHANGES user={key}\n")
                if ui_status:
                    lf.write(f"  UI_STATUS: {ui_status}\n")
                lf.write("  CHANGES:\n")
                for line in changes:
                    lf.write(f"    - {line}\n")
                lf.write("\n")

            self.show_status("Changes saved successfully!", "green")

        except Exception as e:
            tb = traceback.format_exc()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_path, "a", encoding="utf-8") as lf:
                lf.write(f"[{timestamp}] ERROR saving changes: {e}\n")
                lf.write(tb + "\n\n")
            self.show_status("Error saving changes. See changes.log.", "red")

    def show_status(self, message: str, color: str = "green") -> None:
        if hasattr(self, "status_label"):
            self.status_label.destroy()
        self.status_label = ctk.CTkLabel(self.winfo_children()[0], text=message, text_color=color)
        self.status_label.pack(side="left", padx=5)

    def atualizar_interface(self) -> None:
        nome_exibicao = None
        if isinstance(self.usuario_logado, dict):
            nome_exibicao = self.usuario_logado.get("nome") or self.usuario_logado.get("username")
        self.title(f"Admin View - {nome_exibicao or 'Unknown'}")
        try:
            self.atualizar_lista_playlists()
        except Exception:
            pass
        try:
            self.parar()
        except Exception:
            pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bem-vindo ao Arcsound")
        self.geometry("350x450")
        self.resizable(False, False)
        self.setup_imagem_fundo()
        self.setup_widgets()

    def setup_imagem_fundo(self) -> None:
        if not os.path.exists(IMAGEM_FUNDO_PATH):
            print("Imagem de fundo não encontrada!")
            return

        self.imagem_fundo_original = Image.open(IMAGEM_FUNDO_PATH).resize((350, 450))
        self.imagem_fundo_dark = self._aplicar_opacidade(self.imagem_fundo_original.copy(), 0.3)

        img_invertida = ImageOps.invert(self.imagem_fundo_original.convert("RGB"))
        self.imagem_fundo_light = self._aplicar_opacidade(img_invertida, 0.3)

        self.label_fundo = ctk.CTkLabel(self, text="")
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        self.atualizar_fundo()

    def setup_widgets(self) -> None:
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

        self.login_sucesso = ctk.CTkLabel(self, text="")
        self.login_sucesso.pack(pady=10)

    def validar_login(self) -> None:
        usuario = self.insere_usuario.get()
        senha = self.insere_senha.get()

        if usuario == "admin" and senha == "admin":
            self.login_sucesso.configure(text="Admin login successful!", text_color="green")
            tocar_som(SOM_ACERTO, volume=0.2)
            self.after(1000, self.abrir_admin)
            return

        usuarios = carregar_usuarios()
        if usuario in usuarios and usuarios[usuario]["senha"] == senha:
            self.login_sucesso.configure(text="Login realizado com sucesso!", text_color="green")
            tocar_som(SOM_ACERTO, volume=0.2)
            self.after(1000, lambda: self.abrir_player(usuarios[usuario]))
        else:
            self.login_sucesso.configure(text="Usuário ou senha incorretos.", text_color="red")
            tocar_som(SOM_ERRO, volume=0.2)

    def abrir_player(self, usuario_logado: dict) -> None:
        PlayerMusica(self, usuario_logado)
        self.withdraw()

    def abrir_cadastro(self) -> None:
        JanelaCadastro(self)

    def abrir_admin(self) -> None:
        AdminPage(self)
        self.withdraw()

    def alternar_senha(self) -> None:
        if self.insere_senha.cget("show") == "*":
            self.insere_senha.configure(show="")
            self.botao_mostrar_senha.configure(text="Ocultar")
        else:
            self.insere_senha.configure(show="*")
            self.botao_mostrar_senha.configure(text="Mostrar")

    def _aplicar_opacidade(self, img: Image.Image, opacidade: float) -> Image.Image:
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        alpha = img.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacidade)
        img.putalpha(alpha)
        return img

    def atualizar_fundo(self) -> None:
        modo_atual = ctk.get_appearance_mode()
        img = self.imagem_fundo_dark if modo_atual == "Dark" else self.imagem_fundo_light
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(350, 450))
        self.label_fundo.configure(image=img_ctk)

    def alternar_tema(self) -> None:
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