import regex as re
import json

class MusicNotFoundError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class PlaylistAlreadyExistsError(Exception):
    pass


def parse_data_file(filepath):
    usuarios = [] #passar para obj
    playlists = [] #passar para obj
    musicas = [] #passar para obj
    
    current_section = None
    current_playlist = {}
    current_song = {}

    pattern_key_value = re.compile(r"^\s*(?:-)?\s*([\w-]+):\s*(.*)")

    with open(filepath, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue

            if '# Usuários' in linha:
                current_section = 'Usuarios'
                continue
            elif '# Playlists' in linha:
                current_section = 'Playlists'
                continue
            elif '# Músicas' in linha:
                current_section = 'Musicas'
                continue
            elif '---' in linha:
                if current_playlist:
                    playlists.append(current_playlist)
                    current_playlist = {}
                if current_song:
                    musicas.append(current_song)
                    current_song = {}
                current_section = None
                continue

            if current_section == 'Usuarios':
                if linha.startswith('- nome:'):
                    usuarios.append(linha.replace('- nome:', '').strip())

            elif current_section == 'Playlists':
                if linha.startswith('- nome:'):
                    if current_playlist:
                        playlists.append(current_playlist)
                    current_playlist = {}
                
                match = pattern_key_value.match(linha)
                if match:
                    key, value = match.group(1), match.group(2).strip()
                    if key == 'itens':
                        cleaned_value = value.strip('[]')
                        current_playlist[key] = [item.strip() for item in cleaned_value.split(',')]
                    else:
                        current_playlist[key] = value
            
            elif current_section == 'Musicas':
                if linha.startswith('- titulo:'):
                    if current_song:
                        musicas.append(current_song)
                    current_song = {}
                
                match = pattern_key_value.match(linha)
                if match:
                    key = match.group(1).replace('-', '').strip()
                    value = match.group(2).strip()
                    current_song[key] = value
    
    if current_song:
        musicas.append(current_song)
    if current_playlist:
        playlists.append(current_playlist)
        
    return usuarios, playlists, musicas

def validate_playlist_songs(playlists, musicas):
    all_music_titles = {song['titulo'] for song in musicas}
    
    for playlist in playlists:
        for song_title in playlist.get('itens', []):
            if song_title not in all_music_titles:
                raise MusicNotFoundError(f"Erro: A música '{song_title}' na playlist '{playlist['nome']}' não existe.")



if __name__ == "__main__":
    try:
        usuarios, playlists, musicas = parse_data_file('teste.txt')
        print(f"Usuários: {[u for u in usuarios]}")
        print(f"Playlists: {json.dumps(playlists, indent=2, ensure_ascii=False)}")
        print(f"Músicas: {json.dumps(musicas, indent=2, ensure_ascii=False)}")

        try:
            validate_playlist_songs(playlists, musicas)
        except MusicNotFoundError as e:
            print(e)
            
      
    except FileNotFoundError:
        print("Erro: O arquivo não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")