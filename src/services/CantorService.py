from src.models.Cantor import Cantor
from src.dao.CantorDAO import CantorDAO
from src.utils.ErrorResponse import ErrorResponse

class CantorService:
    def __init__(self, daoCantorDependency: CantorDAO):
        self.daoCantorDependency = daoCantorDependency
        print("✅ CantorService initialized")
    
    def createCantor(self, cantorBodyRequest: dict) -> int:
        # Extrai dados do body
        nomeCantor = cantorBodyRequest.get("nomeCantor")
        nacionalidade = cantorBodyRequest.get("nacionalidade")
        idade = cantorBodyRequest.get("idade")
        sexo = cantorBodyRequest.get("sexo")
        gravadora_id = cantorBodyRequest.get("Gravadora_idGravadora")
        feat_id = cantorBodyRequest.get("FeatFamoso_idFeat")
        
        # Validações básicas
        if not nomeCantor or len(nomeCantor) < 2:
            raise ErrorResponse(400, "Nome do cantor deve ter pelo menos 2 caracteres")
        
        if not nacionalidade or len(nacionalidade) < 2:
            raise ErrorResponse(400, "Nacionalidade deve ter pelo menos 2 caracteres")
        
        if not idade:
            raise ErrorResponse(400, "Idade é obrigatória")
        
        if sexo not in ['Masculino', 'Feminino']:
            raise ErrorResponse(400, "Sexo deve ser 'Masculino' ou 'Feminino'")
        
        # Cria objeto Cantor - ✅ ORDEM CORRETA DO CONSTRUTOR
        cantor = Cantor(
            nomeCantor,      # ✅ Posicional 
            nacionalidade,   # ✅ Posicional
            idade,           # ✅ Posicional
            sexo,            # ✅ Posicional
            gravadora_id,    # ✅ Posicional
            feat_id          # ✅ Posicional
            # idCantor não precisa (é None por padrão)
        )
        
        print("✅ CantorService.createCantor()")
        return self.daoCantorDependency.create(cantor)
    
    def updateCantor(self, cantorBodyRequest: dict, idCantor: int) -> bool:
        # Busca cantor existente
        cantor_existente = self.daoCantorDependency.findById(idCantor)
        
        if not cantor_existente:
            raise ErrorResponse(404, "Cantor não encontrado", {"id": idCantor})
        
        # Pega dados novos ou mantém antigos
        nomeCantor = cantorBodyRequest.get("nomeCantor", cantor_existente['nomeCantor'])
        nacionalidade = cantorBodyRequest.get("nacionalidade", cantor_existente['nacionalidade'])
        idade = cantorBodyRequest.get("idade", cantor_existente['idade'])
        sexo = cantorBodyRequest.get("sexo", cantor_existente['sexo'])
        gravadora_id = cantorBodyRequest.get("Gravadora_idGravadora", cantor_existente['Gravadora_idGravadora'])
        feat_id = cantorBodyRequest.get("FeatFamoso_idFeat", cantor_existente['FeatFamoso_idFeat'])
        
        # Validações
        if len(nomeCantor) < 2:
            raise ErrorResponse(400, "Nome do cantor deve ter pelo menos 2 caracteres")
        
        if len(nacionalidade) < 2:
            raise ErrorResponse(400, "Nacionalidade deve ter pelo menos 2 caracteres")
        
        if sexo not in ['Masculino', 'Feminino']:
            raise ErrorResponse(400, "Sexo deve ser 'Masculino' ou 'Feminino'")
        
        # Cria objeto Cantor atualizado - ✅ ORDEM CORRETA
        cantor = Cantor(
            nomeCantor=nomeCantor,
            nacionalidade=nacionalidade,
            idade=idade,
            sexo=sexo,
            gravadora_id=gravadora_id,
            feat_id=feat_id,
            idCantor=idCantor  # ✅ Passa o ID para update
        )
        
        sucesso = self.daoCantorDependency.update(cantor)
        
        if not sucesso:
            raise ErrorResponse(500, "Falha ao atualizar cantor")
        
        print("✅ CantorService.updateCantor()")
        return sucesso
    
    def deleteCantor(self, idCantor: int) -> bool:
        cantor = self.daoCantorDependency.findById(idCantor)
        if not cantor:
            raise ErrorResponse(404, "Cantor não encontrado", {"id": idCantor})
        
        sucesso = self.daoCantorDependency.delete(idCantor)
        print("✅ CantorService.deleteCantor()")
        return sucesso
    
    def findAll(self) -> list[dict]:
        cantores = self.daoCantorDependency.findAll()
        print(f"✅ CantorService.findAll() -> {len(cantores)} registros")
        return cantores
    
    def findById(self, idCantor: int) -> dict | None:
        cantor = self.daoCantorDependency.findById(idCantor)
        
        if not cantor:
            raise ErrorResponse(404, "Cantor não encontrado", {"id": idCantor})
        
        print("✅ CantorService.findById()")
        return cantor