
class Midia:
    
    playlist = []
    historico = []
    
    def __init__(self, titulo:str,artista:str,dura:int, reproductions:None):
        
        self.titulo = titulo
        self.dura = dura
        self.artista = artista
        self.reproductions = reproductions
        
    def __repr__(self):
        return f'Midia(Titulo={self.titulo}, Artista={self.artista}, Duração={self.dura})'
    
    def __str__(self):
        return f"'{self.titulo}', por '{self.artista} durante '{self.dura}'"
    
    def __eq__(self, other):
        if not isinstance(other, Midia):
            return False
        
        return (self.titulo == other.titulo and
                self.artista == other.artista and
                self.dura == other.dura)
        
    def reproduzir (self):
        self.reproductions =+1
        
        print(f"Reproduzindo {self.titulo} por {self.artista}, durante {self.dura} segundos!")
        print("")
#u1.sign("arthussr", "nunes")
#mus1 = Midia("Song A", "Artist 1", 180, 5)
#mus1.reproduzir(u1)
#print(u1.historico)