class FeatFamoso:
    def __init__(self, nomeFeat, cantorFeat, streams, idFeat = None):
        self.nomeFeat = nomeFeat
        self.cantorFeat = cantorFeat
        self.streams = streams
        self.idFeat = idFeat
    
    # Getters
    def getNomeFeat(self):
        return self.nomeFeat
    
    def getCantorFeat(self):
        return self.cantorFeat
    
    def getStreams(self):
        return self.streams

    def getIdFeat(self):
        return self.idFeat
    
    # Setters
    def setNomeFeat(self, nomeFeat):
        try:
            if not isinstance(nomeFeat, str):
                raise ValueError("O nome do feat deve ser uma string.")
            if len(nomeFeat) < 2:
                raise ValueError("O nome deve ter pelo menos 2 caracteres.")
        except ValueError as ve:
            print(ve)
        self.nomeFeat = nomeFeat
    
    def setCantorFeat(self, cantorFeat):
        try:
            if not isinstance(cantorFeat, str):
                raise ValueError("O nome do cantor deve ser uma string.")
            if len(cantorFeat) < 2:
                raise ValueError("O nome deve ter pelo menos 2 caracteres.")
        except ValueError as ve:
            print(ve)
        self.cantorFeat = cantorFeat
    
    def setStreams(self, streams):
        try:
            if not isinstance(streams, str):
                raise ValueError("Streams deve ser uma string.")
        except ValueError as ve:
            print(ve)
        self.streams = streams
    
    def setIdFeat(self, idFeat):
        self.idFeat = idFeat