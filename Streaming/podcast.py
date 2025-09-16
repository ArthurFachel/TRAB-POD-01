from midia import Midia

class Podcast(Midia):
    def __init__(self, host:str, episodio:int, titulo, temporada:int,reproductions:None):
        super().__init__(titulo,  reproductions)
        self.host = host
        self.temporada = temporada
        self.episodio = episodio
        
    def __str__(self):
        return f"Episódio {self.episodio} - {self.temporada}| '{self.titulo}', por  '{self.host}' durante '{self.dura}'"
    
    def __repr__(self):
        return f'Podcast(Host={self.host}, Temporada={self.temporada}, Episódio={self.episodio})'+ super().__repr__()
        
