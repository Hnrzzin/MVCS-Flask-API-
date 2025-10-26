class Cantor:
    def __init__(self, nomeCantor,nacionalidade, idade, sexo, gravadora_id, feat_id, idCantor = None):
        
        self.nomeCantor = nomeCantor
        self.nacionalidade = nacionalidade
        self.idade = idade
        self.sexo = sexo
        self.gravadora_id = gravadora_id  # FK (obrigatória)
        self.feat_id = feat_id            # FK (obrigatória)
        self.idCantor = idCantor
        
    
    # Getters
    def getIdCantor(self):
        return self.idCantor
    
    def getNomeCantor(self):
        return self.nomeCantor
    
    def getNacionalidade(self):
        return self.nacionalidade
    
    def getIdade(self):
        return self.idade
    
    def getSexo(self):
        return self.sexo
    
    def getGravadora_id(self):
        return self.gravadora_id
    
    def getFeat_id(self):
        return self.feat_id
    
    # Setters
    def setNomeCantor(self, nomeCantor):
        self.nomeCantor = nomeCantor
        try:
            if not isinstance(nomeCantor, str):
                raise ValueError("O nome do cantor deve ser uma string.")
            if len(nomeCantor) < 2:
                raise ValueError("O nome do cantor deve ter pelo menos 2 caracteres.")
        except ValueError as ve:
            print(ve)
        self.nomeCantor = nomeCantor
    
    def setNacionalidade(self, nacionalidade):
        self.nacionalidade = nacionalidade
        try:
            if not isinstance(nacionalidade, str):
                raise ValueError("A nacionalidade deve ser uma string.")
            if len(nacionalidade) < 2:  
                raise ValueError("A nacionalidade deve ter pelo menos 2 caracteres.")
        except ValueError as ve:
            print(ve)
        self.nacionalidade = nacionalidade
            
    def setIdade(self, idade):
        self.idade = idade
        try:
            parseInt = int(idade)   
            if not isinstance(parseInt): 
                raise ValueError("A idade deve ser um número inteiro.")
            if parseInt < 18 or parseInt > 80:
                raise ValueError("A idade deve estar entre 18 e 80 anos.")
        except ValueError as ve:
            print(ve)
        self.idade = parseInt 
            
    def setSexo(self, sexo):
        self.sexo = sexo
        try:
            if sexo not in ['Masculino', 'Feminino']:
                raise ValueError("O sexo deve ser 'Masculino' (masculino), 'Feminino' (feminino).")
        except ValueError as ve:
            print(ve)
        self.sexo = sexo
    
    def setId (self, idCantor):
        self.idCantor = idCantor