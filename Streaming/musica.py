from midia import Midia


class Musica(Midia):
    def __init__(self, titulo: str, artista: str, duracao: int, genero: str):
        super().__init__(titulo, artista, duracao, genero)


    def rating(self, avaliar):
        if avaliar > 5: 
            return f"Erro | Insira uma nota de 0 a 5"
        self.avaliacao.append(avaliar)
        return f" Avaliação de {self.avaliacao} atribuída à música '{self.titulo}'."
    
    def __repr__(self):
        return f"Musica(genero='{self.genero}', avaliações={self.avaliacao})" 
    
    def __eq__(self, other):
        if not isinstance(other, Musica):
            return False
    def __str__(self):
        return f"'{self.genero}', nota '{self.avaliacao} '{self.dura}'"
        