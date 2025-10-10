import customtkinter as ctk
from tkinter import filedialog, messagebox
import pygame
import os
from pathlib import Path
import yaml

class PlayerMusica(ctk.CTkToplevel):
    def __init__(self, master, usuario_logado):
        super().__init__(master)
        
        self.usuario_logado = usuario_logado
        self.title(f"Arcsound - {usuario_logado['nome']}")
        self.geometry("900x600")
        
        pygame.mixer.init()
        
        self.musica_atual = None
        self.musicas_biblioteca = []
        self.playlist_atual = None
        self.tocando = False
        self.pausado = False
        
        self.carregar_dados_usuario()
        self.setup_interface()
        
    def carregar_dados_usuario(self):
        """Carrega as playlists e histórico do usuário"""
        self.playlists = self.usuario_logado.get('playlists', [])
        self.historico = self.usuario_logado.get('historico', [])
        
    def salvar_dados_usuario(self):
        """Salva os dados do usuário no arquivo YAML"""
        arquivo_usuarios = "usuarios.yaml"
        if os.path.exists(arquivo_usuarios):
            with open(arquivo_usuarios, 'r', encoding='utf-8') as file:
                usuarios = yaml.safe_load(file) or {}
            
            usuarios[self.usuario_logado['nome']]['playlists'] = self.playlists
            usuarios[self.usuario_logado['nome']]['historico'] = self.historico
            
            with open(arquivo_usuarios, 'w', encoding='utf-8') as file:
                yaml.dump(usuarios, file, allow_unicode=True)
    
    def setup_interface(self):
        """Configura a interface do player"""
        # Frame superior - Informações do usuário
        frame_top = ctk.CTkFrame(self, height=50)
        frame_top.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(frame_top, text=f"Bem-vindo, {self.usuario_logado['nome']}!", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(side="left", padx=10)
        
        ctk.CTkButton(frame_top, text="Sair", command=self.sair, 
                     fg_color="red", hover_color="darkred").pack(side="right", padx=10)
        
        # Frame principal - dividido em 3 colunas
        frame_main = ctk.CTkFrame(self)
        frame_main.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Coluna 1 - Biblioteca de Músicas
        self.setup_biblioteca(frame_main)
        
        # Coluna 2 - Playlists
        self.setup_playlists(frame_main)
        
        # Coluna 3 - Player
        self.setup_player(frame_main)
        
    def setup_biblioteca(self, parent):
        """Configura a seção de biblioteca de músicas"""
        frame_biblioteca = ctk.CTkFrame(parent)
        frame_biblioteca.grid(row=0, column=0, sticky="nsew", padx=5)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        ctk.CTkLabel(frame_biblioteca, text="Biblioteca", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(frame_biblioteca)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(btn_frame, text="+ Adicionar Música", 
                     command=self.adicionar_musica).pack(fill="x", pady=2)
        
        # Campo de busca
        search_frame = ctk.CTkFrame(frame_biblioteca)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        self.entry_busca = ctk.CTkEntry(search_frame, placeholder_text="Buscar música...")
        self.entry_busca.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(search_frame, text="🔍", width=40, 
                     command=self.buscar_musica).pack(side="right")
        
        # Lista de músicas
        self.listbox_biblioteca = ctk.CTkScrollableFrame(frame_biblioteca, label_text="Músicas")
        self.listbox_biblioteca.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Botão para tocar música selecionada
        ctk.CTkButton(frame_biblioteca, text="▶ Tocar Selecionada", 
                     command=self.tocar_da_biblioteca).pack(fill="x", padx=5, pady=5)
        
    def setup_playlists(self, parent):
        """Configura a seção de playlists"""
        frame_playlists = ctk.CTkFrame(parent)
        frame_playlists.grid(row=0, column=1, sticky="nsew", padx=5)
        parent.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_playlists, text="Playlists", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(frame_playlists)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(btn_frame, text="+ Nova Playlist", 
                     command=self.criar_playlist).pack(fill="x", pady=2)
        
        ctk.CTkButton(btn_frame, text="🗑 Deletar Playlist", 
                     command=self.deletar_playlist, fg_color="gray").pack(fill="x", pady=2)
        
        # Lista de playlists
        self.listbox_playlists = ctk.CTkScrollableFrame(frame_playlists, label_text="Minhas Playlists")
        self.listbox_playlists.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.atualizar_lista_playlists()
        
        # Frame para músicas da playlist selecionada
        ctk.CTkLabel(frame_playlists, text="Músicas na Playlist:").pack(pady=(10, 5))
        
        self.listbox_musicas_playlist = ctk.CTkScrollableFrame(frame_playlists)
        self.listbox_musicas_playlist.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Botões de ação da playlist
        btn_playlist_frame = ctk.CTkFrame(frame_playlists)
        btn_playlist_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(btn_playlist_frame, text="+ Adicionar à Playlist", 
                     command=self.adicionar_a_playlist).pack(fill="x", pady=2)
        
        ctk.CTkButton(btn_playlist_frame, text="▶ Tocar Playlist", 
                     command=self.tocar_playlist).pack(fill="x", pady=2)
        
    def setup_player(self, parent):
        """Configura a seção do player"""
        frame_player = ctk.CTkFrame(parent)
        frame_player.grid(row=0, column=2, sticky="nsew", padx=5)
        parent.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(frame_player, text="Player", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Informações da música atual
        self.label_musica_atual = ctk.CTkLabel(frame_player, text="Nenhuma música tocando", 
                                              font=ctk.CTkFont(size=14), wraplength=250)
        self.label_musica_atual.pack(pady=20)
        
        # Controles do player
        controles_frame = ctk.CTkFrame(frame_player)
        controles_frame.pack(pady=20)
        
        self.btn_anterior = ctk.CTkButton(controles_frame, text="⏮", width=50, 
                                         command=self.musica_anterior)
        self.btn_anterior.grid(row=0, column=0, padx=5)
        
        self.btn_play_pause = ctk.CTkButton(controles_frame, text="▶", width=60, 
                                           command=self.play_pause, font=ctk.CTkFont(size=20))
        self.btn_play_pause.grid(row=0, column=1, padx=5)
        
        self.btn_stop = ctk.CTkButton(controles_frame, text="⏹", width=50, 
                                      command=self.parar)
        self.btn_stop.grid(row=0, column=2, padx=5)
        
        self.btn_proxima = ctk.CTkButton(controles_frame, text="⏭", width=50, 
                                        command=self.proxima_musica)
        self.btn_proxima.grid(row=0, column=3, padx=5)
        
        # Controle de volume
        volume_frame = ctk.CTkFrame(frame_player)
        volume_frame.pack(pady=20, fill="x", padx=20)
        
        ctk.CTkLabel(volume_frame, text="Volume:").pack()
        self.slider_volume = ctk.CTkSlider(volume_frame, from_=0, to=1, 
                                          command=self.ajustar_volume)
        self.slider_volume.set(0.5)
        self.slider_volume.pack(fill="x", pady=5)
        
        # Histórico
        ctk.CTkLabel(frame_player, text="Histórico Recente", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        
        self.listbox_historico = ctk.CTkScrollableFrame(frame_player)
        self.listbox_historico.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.atualizar_historico()
        
    def adicionar_musica(self):
        """Adiciona uma música à biblioteca"""
        arquivos = filedialog.askopenfilenames(
            title="Selecione arquivos de música",
            filetypes=[("Arquivos de Áudio", "*.mp3 *.wav *.ogg")]
        )
        
        for arquivo in arquivos:
            if arquivo not in self.musicas_biblioteca:
                self.musicas_biblioteca.append(arquivo)
                nome_arquivo = Path(arquivo).stem
                
                btn = ctk.CTkButton(self.listbox_biblioteca, text=nome_arquivo, 
                                   anchor="w", command=lambda a=arquivo: self.selecionar_musica(a))
                btn.pack(fill="x", pady=2)
        
        if arquivos:
            messagebox.showinfo("Sucesso", f"{len(arquivos)} música(s) adicionada(s)!")
    
    def buscar_musica(self):
        """Busca músicas na biblioteca"""
        termo = self.entry_busca.get().lower()
        
        for widget in self.listbox_biblioteca.winfo_children():
            widget.destroy()
        
        for musica in self.musicas_biblioteca:
            nome = Path(musica).stem.lower()
            if termo in nome:
                btn = ctk.CTkButton(self.listbox_biblioteca, text=Path(musica).stem, 
                                   anchor="w", command=lambda a=musica: self.selecionar_musica(a))
                btn.pack(fill="x", pady=2)
    
    def selecionar_musica(self, caminho):
        """Seleciona uma música da biblioteca"""
        self.musica_selecionada = caminho
        messagebox.showinfo("Selecionado", f"Música selecionada: {Path(caminho).stem}")
    
    def tocar_da_biblioteca(self):
        """Toca a música selecionada da biblioteca"""
        if hasattr(self, 'musica_selecionada'):
            self.tocar_musica(self.musica_selecionada)
        else:
            messagebox.showwarning("Aviso", "Selecione uma música primeiro!")
    
    def tocar_musica(self, caminho):
        """Toca uma música específica"""
        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.play()
            self.musica_atual = caminho
            self.tocando = True
            self.pausado = False
            self.btn_play_pause.configure(text="⏸")
            
            nome_musica = Path(caminho).stem
            self.label_musica_atual.configure(text=f"🎵 Tocando:\n{nome_musica}")
            
            # Adicionar ao histórico
            if caminho not in self.historico:
                self.historico.insert(0, caminho)
                self.historico = self.historico[:10]  # Manter apenas os 10 últimos
                self.salvar_dados_usuario()
                self.atualizar_historico()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível tocar a música: {e}")
    
    def play_pause(self):
        """Pausa ou retoma a reprodução"""
        if self.tocando:
            if self.pausado:
                pygame.mixer.music.unpause()
                self.pausado = False
                self.btn_play_pause.configure(text="⏸")
            else:
                pygame.mixer.music.pause()
                self.pausado = True
                self.btn_play_pause.configure(text="▶")
        else:
            messagebox.showwarning("Aviso", "Nenhuma música está tocando!")
    
    def parar(self):
        """Para a reprodução"""
        pygame.mixer.music.stop()
        self.tocando = False
        self.pausado = False
        self.btn_play_pause.configure(text="▶")
        self.label_musica_atual.configure(text="Nenhuma música tocando")
    
    def ajustar_volume(self, valor):
        """Ajusta o volume"""
        pygame.mixer.music.set_volume(float(valor))
    
    def criar_playlist(self):
        """Cria uma nova playlist"""
        dialog = ctk.CTkInputDialog(text="Nome da nova playlist:", title="Nova Playlist")
        nome = dialog.get_input()
        
        if nome:
            nova_playlist = {
                'nome': nome,
                'musicas': []
            }
            self.playlists.append(nova_playlist)
            self.salvar_dados_usuario()
            self.atualizar_lista_playlists()
            messagebox.showinfo("Sucesso", f"Playlist '{nome}' criada!")
    
    def atualizar_lista_playlists(self):
        """Atualiza a lista de playlists"""
        for widget in self.listbox_playlists.winfo_children():
            widget.destroy()
        
        for playlist in self.playlists:
            btn = ctk.CTkButton(self.listbox_playlists, text=f"📁 {playlist['nome']}", 
                               anchor="w", command=lambda p=playlist: self.selecionar_playlist(p))
            btn.pack(fill="x", pady=2)
    
    def selecionar_playlist(self, playlist):
        """Seleciona uma playlist"""
        self.playlist_atual = playlist
        
        # Atualizar lista de músicas da playlist
        for widget in self.listbox_musicas_playlist.winfo_children():
            widget.destroy()
        
        for musica in playlist['musicas']:
            nome = Path(musica).stem if os.path.exists(musica) else musica
            btn = ctk.CTkButton(self.listbox_musicas_playlist, text=nome, 
                               anchor="w", command=lambda m=musica: self.tocar_musica(m))
            btn.pack(fill="x", pady=2)
        
        messagebox.showinfo("Playlist", f"Playlist '{playlist['nome']}' selecionada!\n"
                           f"Músicas: {len(playlist['musicas'])}")
    
    def adicionar_a_playlist(self):
        """Adiciona música selecionada à playlist atual"""
        if not self.playlist_atual:
            messagebox.showwarning("Aviso", "Selecione uma playlist primeiro!")
            return
        
        if not hasattr(self, 'musica_selecionada'):
            messagebox.showwarning("Aviso", "Selecione uma música primeiro!")
            return
        
        if self.musica_selecionada not in self.playlist_atual['musicas']:
            self.playlist_atual['musicas'].append(self.musica_selecionada)
            self.salvar_dados_usuario()
            self.selecionar_playlist(self.playlist_atual)
            messagebox.showinfo("Sucesso", "Música adicionada à playlist!")
        else:
            messagebox.showinfo("Info", "Música já está na playlist!")
    
    def tocar_playlist(self):
        """Toca a primeira música da playlist"""
        if not self.playlist_atual:
            messagebox.showwarning("Aviso", "Selecione uma playlist primeiro!")
            return
        
        if not self.playlist_atual['musicas']:
            messagebox.showwarning("Aviso", "A playlist está vazia!")
            return
        
        self.tocar_musica(self.playlist_atual['musicas'][0])
    
    def deletar_playlist(self):
        """Deleta a playlist selecionada"""
        if not self.playlist_atual:
            messagebox.showwarning("Aviso", "Selecione uma playlist primeiro!")
            return
        
        resposta = messagebox.askyesno("Confirmar", 
                                       f"Deseja deletar a playlist '{self.playlist_atual['nome']}'?")
        if resposta:
            self.playlists.remove(self.playlist_atual)
            self.playlist_atual = None
            self.salvar_dados_usuario()
            self.atualizar_lista_playlists()
            
            for widget in self.listbox_musicas_playlist.winfo_children():
                widget.destroy()
            
            messagebox.showinfo("Sucesso", "Playlist deletada!")
    
    def musica_anterior(self):
        """Toca a música anterior da playlist"""
        if self.playlist_atual and self.playlist_atual['musicas']:
            try:
                idx = self.playlist_atual['musicas'].index(self.musica_atual)
                if idx > 0:
                    self.tocar_musica(self.playlist_atual['musicas'][idx - 1])
            except ValueError:
                pass
    
    def proxima_musica(self):
        """Toca a próxima música da playlist"""
        if self.playlist_atual and self.playlist_atual['musicas']:
            try:
                idx = self.playlist_atual['musicas'].index(self.musica_atual)
                if idx < len(self.playlist_atual['musicas']) - 1:
                    self.tocar_musica(self.playlist_atual['musicas'][idx + 1])
            except ValueError:
                pass
    
    def atualizar_historico(self):
        """Atualiza a lista de histórico"""
        for widget in self.listbox_historico.winfo_children():
            widget.destroy()
        
        for musica in self.historico[:5]:
            nome = Path(musica).stem if os.path.exists(musica) else musica
            btn = ctk.CTkButton(self.listbox_historico, text=nome, 
                               anchor="w", command=lambda m=musica: self.tocar_musica(m))
            btn.pack(fill="x", pady=2)
    
    def sair(self):
        """Sai do player"""
        pygame.mixer.music.stop()
        self.destroy()
