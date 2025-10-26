class Gravadora:
    def __init__(self, nomeGravadora, localizacao, idGravadora = None):
        self.nomeGravadora = nomeGravadora
        self.localizacao = localizacao
        self.idGravadora = idGravadora
    # Getters
    def getNomeGravadora(self):
        return self.nomeGravadora
    
    def getLocalizacao(self):
        return self.localizacao
    
    def getIdGravadora(self):
        return self.idGravadora
    
    # Setters
    def setNomeGravadora(self, nomeGravadora):
        try:
            if not isinstance(nomeGravadora, str):
                raise ValueError("O nome da gravadora deve ser uma string.")
            if len(nomeGravadora) < 2:
                raise ValueError("O nome deve ter pelo menos 2 caracteres.")
        except ValueError as ve:
            print(ve)
        self.nomeGravadora = nomeGravadora
    
    def setLocalizacao(self, localizacao):
        try:
            if not isinstance(localizacao, str):
                raise ValueError("A localização deve ser uma string.")
            if len(localizacao) < 2:
                raise ValueError("A localização deve ter pelo menos 2 caracteres.")
        except ValueError as ve:
            print(ve)
        self.localizacao = localizacao
    
    def setIdGravadora(self, idGravadora):
        self.idGravadora = idGravadora