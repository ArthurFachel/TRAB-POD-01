import secrets
from midia import Midia

class User:
    user_list = []
    
    def __init__(self, nome=None, password=None, token=None):
        self.nome = nome
        self.historico = []      # histórico de mídias ouvidas
        self.playlists = {} 
        self.password = password
        self.token = token

    def ouvir_midia(self, midia: Midia):
        midia.reproduzir()  # incrementa contagem da mídia
        self.historico.append(midia)
        print(f" {self.nome} ouviu '{midia.titulo}' de {midia.artista}")

    def criar_playlist(self, nome: str):
        if nome in self.playlists:
            print(f"Playlist '{nome}' já existe.")
        else:
            self.playlists[nome] = []
            print(f" Playlist '{nome}' criada com sucesso!")

    def adicionar_a_playlist(self, nome: str, midia: Midia):
        if nome not in self.playlists:
            print(f" '{nome}' não existe.")
            return
        self.playlists[nome].append(midia)
        print(f"➕ '{midia.titulo}' adicionado à playlist '{nome}'.")

    def ver_playlists(self):
        if not self.playlists:
            print("Nenhuma playlist criada ainda.")
            return
        for nome, musicas in self.playlists.items():
            print(f"\n Playlist: {nome}")
            for m in musicas:
                print(f"   - {m.titulo} ({m.artista})")

        
    @classmethod
    def n_instance(cls):
        
       return len(cls.user_list)
   
   
    @classmethod
    def is_user_exist(cls, name:str)->bool:
        for user in cls.user_list:
            if user["name"] == name:
             return True
        return False

    def sign(self, user, password):
        if self.is_user_exist(user):
            print(f"❌ User '{user}' already exists!")
            return None
        self.user = user
        self.password = password
        self.token = secrets.token_hex(16)
        
        self.user_list.append({"name": self.user, "token": self.token})
        return self.token
    
