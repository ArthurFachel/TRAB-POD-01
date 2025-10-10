from typing import List, Optional
from .midia import Midia
from .musica import Musica

class Playlist:
    def __init__(self, nome: str, criador: str):
        self.nome = nome
        self.criador = criador
        self.midias: List[Midia] = []
        self.reproducoes = 0
        self.atual_index = -1

    def adicionar_midia(self, midia: Midia) -> None:
        """Adiciona uma mídia à playlist."""
        if midia not in self.midias:
            self.midias.append(midia)

    def remover_midia(self, midia: Midia) -> bool:
        """Remove uma mídia da playlist. Retorna True se removida com sucesso."""
        if midia in self.midias:
            self.midias.remove(midia)
            return True
        return False

    def proxima_midia(self) -> Optional[Midia]:
        """Retorna a próxima mídia na playlist."""
        if not self.midias:
            return None
        
        self.atual_index = (self.atual_index + 1) % len(self.midias)
        return self.midias[self.atual_index]

    def midia_anterior(self) -> Optional[Midia]:
        """Retorna a mídia anterior na playlist."""
        if not self.midias:
            return None
        
        self.atual_index = (self.atual_index - 1) % len(self.midias)
        return self.midias[self.atual_index]

    def get_midia_atual(self) -> Optional[Midia]:
        if not self.midias or self.atual_index < 0:
            return None
        return self.midias[self.atual_index]

    def limpar(self) -> None:
        self.midias.clear()
        self.atual_index = -1

    def reproduzir(self) -> None:
        self.reproducoes += 1

    def quantidade_midias(self) -> int:
        return len(self.midias)

    def get_duracao_total(self) -> int:
        return sum(midia.duracao for midia in self.midias)

    def to_dict(self) -> dict:
        return {
            'nome': self.nome,
            'criador': self.criador,
            'midias': [midia.titulo for midia in self.midias],
            'reproducoes': self.reproducoes
        }

    @staticmethod
    def from_dict(data: dict, todas_midias: List[Midia]) -> 'Playlist':
        playlist = Playlist(data['nome'], data['criador'])
        playlist.reproducoes = data.get('reproducoes', 0)
        
        # Adiciona as mídias baseado nos títulos salvos
        for titulo in data.get('midias', []):
            for midia in todas_midias:
                if midia.titulo == titulo:
                    playlist.adicionar_midia(midia)
                    break
        
        return playlist

    def __str__(self) -> str:
        return f"Playlist: {self.nome} (por {self.criador}) - {len(self.midias)} mídias"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Playlist):
            return False
        return self.nome == other.nome and self.criador == other.criador

from .midia import Midia
class Podcast(Midia):
    def __init__(self, titulo, duracao, artista, reproducoes=None, ):
        super().__init__(titulo, duracao, artista)
        self.reproducoes = reproducoes