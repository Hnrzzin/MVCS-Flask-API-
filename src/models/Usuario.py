class Usuario:
    def __init__(self, nome, email, senha, idUsuario=None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.idUsuario = idUsuario
    
    def getIdUsuario(self):
        return self.idUsuario
    
    def getNome(self):
        return self.nome
    
    def getEmail(self):
        return self.email
    
    def getSenha(self):
        return self.senha
    
    
    # Setters 
    def setIdUsuario(self, idUsuario):
        self.idUsuario = idUsuario
        
    def setNome(self, nome):
        self.nome = nome
        try:
            if not isinstance(nome, str):
                raise ValueError("O nome deve ser uma string.")
            if len(nome) < 2:
                raise ValueError("O nome deve ter pelo menos 2 caracteres.")
        except ValueError as ve:
            print(ve)
        self.nome = nome
    
    def setEmail(self, email):
        self.email = email
        try:
            if not isinstance(email, str):
                raise ValueError("O email deve ser uma string.")
            if "@" not in email or "." not in email:
                raise ValueError("O email deve ser um endereço de email válido.")
        except ValueError as ve:
            print(ve)
        self.email = email
        
    def setSenha(self, senha):
        self.senha = senha
        try:
            if len(senha) < 6:
                raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        except ValueError as ve:
            print(ve)
        self.senha = senha