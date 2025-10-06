class User  :
    def __init__(self, nome, senha, inst=None, historico=None, playlists=None):
        self.nome = nome
        self.senha = senha
        self.inst = inst
        self.historico = historico if historico is not None else []
        self.playlists = playlists if playlists is not None else []
    def __str__(self):
        return f"Usuário: {self.nome} - Instancias: {self.inst} - Historico: {self.historico} - Playlists: {self.playlists}"
    
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'senha': self.senha,
            'inst': self.inst,
            'historico': self.historico,
            'playlists': self.playlists
        }
    def addUser(self, nome, senha, inst):
        self.nome = nome
        self.senha = senha
        self.inst = inst
        
user = User("Arthur", '123')