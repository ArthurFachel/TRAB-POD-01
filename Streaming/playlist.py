# Playlist.py
from midia import Midia
from usuario import User

class Playlist(Midia):
    def __init__(self, nome: str, itens: list, user: User):
        super().__init__(titulo=None, artista=None, dura=None, reproductions=0)
        self.nome = nome
        self.itens = itens
        self.user = user
        self.reproductions = 0

    def __repr__(self):
        return f'Playlist(Nome={self.nome}, Midias={self.itens})'

    def __str__(self):
        return f"'{self.nome}', com '{len(self.itens)}' mídias"

    def adicionar_midia(self, midia: Midia):
        if not isinstance(midia, Midia):
            print("Erro | O item a ser adicionado não é uma mídia.")
            return
        self.itens.append(midia)
        print(f"✅ Mídia '{midia.titulo}' adicionada à playlist '{self.nome}'.")

    def remover_midia(self, midia: Midia):
        if not isinstance(midia, Midia):
            print("Erro | O item a ser removido não é uma mídia.")
            return
        if midia in self.itens:
            self.itens.remove(midia)
            print(f"Mídia '{midia.titulo}' removida da playlist '{self.nome}'.")
        else:
            print(f"Mídia '{midia.titulo}' não encontrada na playlist '{self.nome}'.")

    def __add__(self, other):
        if not isinstance(other, Playlist):
            print("Erro | Não é possível somar uma playlist com um item que não seja uma playlist.")
            return self
        
        novo_nome = f"{self.nome} & {other.nome}"
        novos_itens = self.itens + other.itens
        
        return Playlist(nome=novo_nome, itens=novos_itens, user=self.user)

    def __len__(self):
        return len(self.itens)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.itens[index.start:index.stop:index.step]
        return self.itens[index]

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        
        return (self.nome == other.nome and
                sorted(self.itens, key=lambda x: x.titulo) == sorted(other.itens, key=lambda x: x.titulo) and
                self.user.name == other.user.name)

    def reproduzir(self, usuario: User):
        """Sobrescreve o método 'reproduzir' da classe pai (Midia)"""
        print(f"Iniciando a reprodução da playlist '{self.nome}'...")
        for midia in self.itens:
            midia.reproduzir(usuario)
        self.reproductions += 1