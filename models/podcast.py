from .midia import Midia 
class Podcast(Midia):
    def __init__(self, titulo: str, duracao: float, artista: str, host: str, episodios: int):
        super().__init__(titulo, duracao, artista)
        self.host = host
        self.episodios = episodios

    def __str__(self):
        return f"{self.titulo} — {self.artista} - ({self.duracao} segundos) | Host: {self.host} | Episódios: {self.episodios}"