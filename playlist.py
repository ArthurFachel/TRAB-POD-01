from midia import Midia
class Podcast(Midia):
    def __init__(self, titulo, duracao, artista, reproducoes=None, ):
        super().__init__(titulo, duracao, artista)
        self.reproducoes = reproducoes  