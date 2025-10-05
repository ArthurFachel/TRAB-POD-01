class User  :
    def __init__(self, nome, senha, inst, historico=None, playlists=None):
        self.nome = nome
        self.senha = senha
        self.inst = inst
        self.historico = historico if historico is not None else []
        self.playlists = playlists if playlists is not None else []
    def __str__(self):
        return f"Usuário: {self.nome} - Instancias: {self.inst} - Historico: {self.historico} - Playlists: {self.playlists}"