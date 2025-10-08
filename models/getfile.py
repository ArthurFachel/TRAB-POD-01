import regex as re
import json
from .user import User
from .musica import Musica

filepath = 'aaa.md'

class MusicNotFoundError(Exception):
    pass

def parse_data_file(filepath):
    usuarios = []
    playlists = []
    musicas = []
    podcasts = []

    current_section = None
    temp_obj = {}

    pattern_key_value = re.compile(r"^\s*(?:-)?\s*([\w-]+):\s*(.*)")

    def flush_obj():
        nonlocal temp_obj
        if current_section == 'Usuarios' and temp_obj:
            usuarios.append(User(
                nome=temp_obj.get('nome'),
                senha=temp_obj.get('senha'),
                playlists=temp_obj.get('playlists', [])
            ))
        elif current_section == 'Playlists' and temp_obj:
            playlists.append(temp_obj.copy())
        elif current_section == 'Musicas' and temp_obj:
            musicas.append(Musica(
                titulo=temp_obj.get('titulo'),
                artista=temp_obj.get('artista'),
                duracao=int(temp_obj.get('duracao', 0)),
                genero=temp_obj.get('genero')
            ))
        elif current_section == 'Podcasts' and temp_obj:
            podcasts.append(temp_obj.copy())
        temp_obj = {}

    with open(filepath, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                if current_section and temp_obj:
                    flush_obj()
                continue

            if 'Usuários' in linha:
                if current_section and temp_obj:
                    flush_obj()
                current_section = 'Usuarios'
                continue
            elif 'Playlists' in linha:
                if current_section and temp_obj:
                    flush_obj()
                current_section = 'Playlists'
                continue
            elif 'Músicas' in linha:
                if current_section and temp_obj:
                    flush_obj()
                current_section = 'Musicas'
                continue
            elif 'Podcasts' in linha:
                if current_section and temp_obj:
                    flush_obj()
                current_section = 'Podcasts'
                continue
            elif linha == '---':
                if current_section and temp_obj:
                    flush_obj()
                current_section = None
                continue

            match = pattern_key_value.match(linha)
            if not match:
                continue

            key, value = match.group(1), match.group(2).strip()

            if current_section == 'Usuarios':
                if key in ['nome', 'senha']:
                    temp_obj[key] = value
                elif key == 'playlists':
                    temp_obj[key] = [item.strip() for item in value.strip('[]').split(',') if item.strip()]
            elif current_section == 'Playlists':
                if key == 'itens':
                    temp_obj[key] = [item.strip() for item in value.strip('[]').split(',') if item.strip()]
                else:
                    temp_obj[key] = value
            elif current_section == 'Musicas':
                temp_obj[key] = value
            elif current_section == 'Podcasts':
                temp_obj[key] = value

        if current_section and temp_obj:
            flush_obj()  # flush last object

    return usuarios, playlists, musicas, podcasts

def validate_playlist_items(playlists, musicas, podcasts):
    all_titles = {m.titulo for m in musicas} | {p.get('titulo') for p in podcasts}
    for playlist in playlists:
        for item_title in playlist.get('itens', []):
            if item_title not in all_titles:
                raise MusicNotFoundError(
                    f"Erro: O item '{item_title}' na playlist '{playlist.get('nome', '')}' não existe."
                )

if __name__ == "__main__":
    try:
        usuarios, playlists, musicas, podcasts = parse_data_file(filepath)

        print("\nUsuarios:  ")
        for u in usuarios:
            print(u)

        print("\nPlaylists:")
        print(json.dumps(playlists, indent=2, ensure_ascii=False))

        print("\n Músicas:")
        for m in musicas:
            print(m)

        print("\nPodcasts")
        print(json.dumps(podcasts, indent=2, ensure_ascii=False))

        validate_playlist_items(playlists, musicas, podcasts)

    except FileNotFoundError:
        print("Erro: O arquivo não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")