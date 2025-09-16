import hashlib
import secrets


class User:
    user_list = []
    def __init__(self, name=None, password=None,token=None):
        self.name = name
        self.password = password
        self.token = token
        
        
    @classmethod
    def is_user_exist(cls, name:str)->bool:
        for user in cls.user_list:
            if user["name"] == name:
             return True
        return False
    
    @classmethod
    def n_instance(cls):
        
       return len(cls.user_list)
    
    @staticmethod
    def encrypt(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def sign(self, user: str, password: str):
        if self.is_user_exist(user):
            print(f"❌ User '{user}' already exists!")
            return None
        self.user = user
        self.hashed_password = self.encrypt(password)
        self.token = secrets.token_hex(16)
        
        self.user_list.append({"name": self.user, "token": self.token})
        return self.token
    
    
#Teste    
u = User()
token = u.sign("arthur", "minhasenha")

print(User.n_instance())