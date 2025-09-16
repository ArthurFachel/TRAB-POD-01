from musica import Musica
from playlist import Playlist
from usuario import User  

class Analise:

    @staticmethod
    def top_musicas_reproduzidas(musicas, top_n):
        return sorted(musicas, key=lambda m: m.reproducoes, reverse=True)[:top_n]

    @staticmethod
    def playlist_mais_popular(playlists):
        if not playlists:
            return None
        return max(playlists, key=lambda p: p.reproducoes)

    @staticmethod
    def usuario_mais_ativo(usuarios):
        if not usuarios:
            return None
        return max(usuarios, key=lambda u: len(u.historico))

    @staticmethod
    def media_avaliacoes(musicas):
        medias = {}
        for m in musicas:
            if hasattr(m, "avaliacoes") and m.avaliacoes: 
                medias[m.titulo] = sum(m.avaliacoes) / len(m.avaliacoes)
            else:
                medias[m.titulo] = 0.0
        return medias

    @staticmethod
    def total_reproducoes(usuarios):
        return sum(len(u.historico) for u in usuarios)
