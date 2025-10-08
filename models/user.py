class User:
    def __init__(self, nome, senha, email=None, inst=None, historico=None, playlists=None):
        self.nome = nome
        self.senha = senha
        self.email = email  #+ -> atributo email
        self.inst = inst
        self.historico = historico if historico is not None else []
        self.playlists = playlists if playlists is not None else []

    def __str__(self):
        return f"Usuário: {self.nome} - Email: {self.email} - Instancias: {self.inst}"

    def to_dict(self):
        """Converte a instância do usuário para um dicionário."""
        return {
            'nome': self.nome,
            'senha': self.senha,
            'email': self.email,
            'inst': self.inst,
            'historico': self.historico,
            'playlists': self.playlists
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data.get('nome'),
            senha=data.get('senha'),
            email=data.get('email'),
            inst=data.get('inst'),
            historico=data.get('historico'),
            playlists=data.get('playlists')
        )