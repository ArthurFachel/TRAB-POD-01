from typing import List, Dict, Optional
import os
import yaml
from statistics import mean

ARQUIVO_USUARIOS = "usuarios.yaml"

def _load_data() -> dict:
    """Carrega os dados do arquivo YAML de forma segura."""
    if not os.path.exists(ARQUIVO_USUARIOS):
        return {}
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except (IOError, yaml.YAMLError):
        return {}

def top_musicas_reproduzidas(top_n: int = 10) -> List[Dict]:
    """Retorna uma lista das músicas mais reproduzidas."""
    data = _load_data()
    usuarios = {k: v for k, v in data.items() if k != "BIBLIOTECA"}
    biblioteca = data.get("BIBLIOTECA", []) or []
    counts: Dict[str, int] = {}

    for u in usuarios.values():
        historico = u.get("historico", []) or []
        for t in historico:
            # Converte o item do histórico para string para contagem,
            # seja ele um dict ou uma str.
            titulo = t.get('titulo') if isinstance(t, dict) else str(t)
            if titulo:
                counts[titulo] = counts.get(titulo, 0) + 1

    for m in biblioteca:
        # VERIFICAÇÃO ADICIONADA: Ignora itens que não são dicionários.
        if not isinstance(m, dict):
            continue
        if m.get("tipo") == "musica":
            counts.setdefault(m.get("titulo"), 0)

    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [{"titulo": t, "reproducoes": r} for t, r in sorted_items[:top_n]]

def playlist_mais_popular() -> Optional[Dict]:
    """Encontra a playlist com o maior número de reproduções de suas músicas."""
    data = _load_data()
    usuarios = {k: v for k, v in data.items() if k != "BIBLIOTECA"}
    global_hist = []
    for u in usuarios.values():
        if isinstance(u, dict):
            global_hist.extend(u.get("historico", []) or [])
    
    # Normaliza o histórico para conter apenas strings de títulos
    normalized_hist = []
    for item in global_hist:
        if isinstance(item, dict):
            normalized_hist.append(item.get('titulo'))
        else:
            normalized_hist.append(str(item))

    best_playlist = None
    best_count = -1

    for username, user in usuarios.items():
        if not isinstance(user, dict):
            continue
        for pl in user.get("playlists", []) or []:
            # VERIFICAÇÃO ADICIONADA: Ignora playlists que não são dicionários.
            if not isinstance(pl, dict):
                continue

            nome = pl.get("nome")
            musicas = pl.get("musicas", []) or []
            
            # Conta quantas vezes as músicas da playlist aparecem no histórico
            count = sum(normalized_hist.count(m) for m in musicas)
            
            if count > best_count:
                best_count = count
                best_playlist = {
                    "nome": nome,
                    "usuario": username,
                    "musicas": musicas,
                    "reproducoes": count
                }
    return best_playlist

def usuario_mais_ativo() -> Optional[Dict]:
    """Encontra o usuário com o maior histórico de reproduções."""
    data = _load_data()
    usuarios = {k: v for k, v in data.items() if k != "BIBLIOTECA"}
    best_user = None
    best_count = -1

    for key, user in usuarios.items():
        if not isinstance(user, dict):
            continue

        hist_count = len(user.get("historico", []) or [])
        if hist_count > best_count:
            best_count = hist_count
            best_user = user.copy()
            best_user["nome"] = key
            best_user["total_reproducoes"] = hist_count
            
    return best_user

def media_avaliacoes() -> Dict[str, float]:
    """Calcula a média de avaliações para cada música na biblioteca."""
    data = _load_data()
    biblioteca = data.get("BIBLIOTECA", []) or []
    medias: Dict[str, float] = {}

    for m in biblioteca:
        if not isinstance(m, dict):
            continue
        
        titulo = m.get("titulo")
        if not titulo or m.get("tipo") != "musica":
            continue
            
        avaliacoes = m.get("avaliacoes", []) or []
        if avaliacoes:
            numeric_avals = [v for v in avaliacoes if isinstance(v, (int, float))]
            if numeric_avals:
                medias[titulo] = mean(numeric_avals)
            else:
                medias[titulo] = 0.0
        else:
            medias[titulo] = 0.0
            
    return medias

def total_reproducoes() -> int:
    """Calcula o total de reproduções de todos os usuários."""
    data = _load_data()
    usuarios = {k: v for k, v in data.items() if k != "BIBLIOTECA"}
    total = 0
    for user in usuarios.values():
        if isinstance(user, dict):
            total += len(user.get("historico", []) or [])
    return total