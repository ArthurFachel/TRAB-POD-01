from .midia import Midia

class Musica(Midia):
    def __init__(self, titulo, artista, duracao, genero):
        super().__init__(titulo, artista, duracao)
        self.genero = genero
        self.avaliacoes: list[int] = []

    def avaliar(self, nota: int):
        if 0 <= nota <= 5:
            self.avaliacoes.append(nota)
        else:
            raise ValueError("A nota deve estar entre 0 e 5.")

    def media_avaliacoes(self):
        if not self.avaliacoes:
            return None
        return sum(self.avaliacoes) / len(self.avaliacoes)

    def __str__(self):
        media = self.media_avaliacoes()
        media_str = f"{media:.1f}" if media is not None else "Sem avaliações"
        return f"{self.titulo} — {self.artista} - ({self.duracao} segundos) | Gênero: {self.genero} | Média: {media_str}"
        



m1 = Musica("Bohemian Rhapsody", "Queen" ,355, "Rock")

m1.reproduzir()
m1.avaliar(5)
m1.avaliar(4)
m1.avaliar(5)

print(m1)