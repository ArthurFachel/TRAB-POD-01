class Midia:
    def __init__(self, titulo, artista, duracao):
        self.titulo = titulo
        self.artista = artista
        self.duracao = duracao

    def reproduzir(self):
        print(f"🎵 Reproduzindo: {self.titulo} — {self.artista} ({self.duracao} segundos)")

    
    def __str__(self):
        return f"{self.titulo} — {self.artista} - {self.duracao}  segundos"

    def __eq__(self, value):
       if isinstance(value, Midia):
            return self.titulo == value.titulo and self.titulo == value.titulo
       return False