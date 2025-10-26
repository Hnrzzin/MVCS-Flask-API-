from src.models.Cantor import Cantor
from src.dao.CantorDAO import CantorDAO
from src.utils.ErrorResponse import ErrorResponse

class CantorService:
    
    def __init__(self, daoCantorDependency: CantorDAO):
        self.daoCantorDependency = daoCantorDependency
        print("✅ CantorService initialized")
        
        
    # Create    
    def createCantor(self, cantorBodyRequest: dict) -> int:
        
        # Extrai dados do body request
        nomeCantor = cantorBodyRequest.get("nomeCantor")
        nacionalidade = cantorBodyRequest.get("nacionalidade")
        idade = cantorBodyRequest.get("idade")
        sexo = cantorBodyRequest.get("sexo")
        gravadora_id = cantorBodyRequest.get("gravadora_id")
        feat_id = cantorBodyRequest.get("feat_id")
        
        # Validações
        if not nomeCantor or len(nomeCantor) < 2:
            raise ErrorResponse(400,
                                "Nome do cantor deve ter pelo menos 2 caracteres"
                                )
        
        if not nacionalidade or len(nacionalidade) < 2:
            raise ErrorResponse(400,
                                "Nacionalidade deve ter pelo menos 2 caracteres"
                                )
        
        if not isinstance(idade, int) or idade <= 0:
            raise ErrorResponse(400,
                                "Idade deve ser um número inteiro positivo"
                                )
        
        if sexo not in ['Masculino', 'Feminino']:
            raise ErrorResponse(400,
                                "Sexo deve ser 'Mascilino' ou 'Feminino'"
                                )
        
        if not gravadora_id or not isinstance(gravadora_id, int):
            raise ErrorResponse(400,
                                "gravadora_id inválido"
                                )
        
        if not feat_id or not isinstance(feat_id, int):
            raise ErrorResponse(400,
                                "feat_id inválido"
                                )
        
        # Cria objeto Cantor populado
        cantor = Cantor(
            nomeCantor=nomeCantor,
            nacionalidade=nacionalidade,
            idade=idade,
            sexo=sexo,
            gravadora_id=gravadora_id,
            feat_id=feat_id
        )
        
        print("✅ CantorService.createCantor()")
        return self.daoCantorDependency.create(cantor)
    
    
    # Update
    def updateCantor(self, cantorBodyRequest: dict, idCantor: int) -> bool:
        
        # Busca cantor existente
        cantorExistente = self.daoCantorDependency.findById(idCantor)
        if not cantorExistente:
            raise ErrorResponse(404,
                                "Cantor não encontrado",
                                {"id": idCantor}
                                )
        
        # Extrai dados do body request
        nomeCantor = cantorBodyRequest.get("nomeCantor", cantorExistente['nomeCantor'])
        nacionalidade = cantorBodyRequest.get("nacionalidade", cantorExistente['nacionalidade'])
        idade = cantorBodyRequest.get("idade", cantorExistente['idade'])
        sexo = cantorBodyRequest.get("sexo", cantorExistente['sexo'])
        gravadora_id = cantorBodyRequest.get("gravadora_id", cantorExistente['gravadora_id'])
        feat_id = cantorBodyRequest.get("feat_id", cantorExistente['feat_id'])
        
        # Validações
        if not nomeCantor or len(nomeCantor) < 2:
            raise ErrorResponse(400,
                                "Nome do cantor deve ter pelo menos 2 caracteres"
                                )
        verificarCantorExistente = self.daoCantorDependency.findByNome(nomeCantor)
        
        if verificarCantorExistente and verificarCantorExistente['id'] != idCantor:
            raise ErrorResponse(400,
                                "Já existe um cantor com esse nome",
                                {"nomeCantor": nomeCantor}
                                )
        
        if not nacionalidade or len(nacionalidade) < 2:
            raise ErrorResponse(400,
                                "Nacionalidade deve ter pelo menos 2 caracteres"
                                )
        
        if not isinstance(idade, int) or idade <= 0:
            raise ErrorResponse(400,
                                "Idade deve ser um número inteiro positivo"
                                )
        
        if sexo not in ['Masculino', 'Feminino']:
            raise ErrorResponse(400,
                                "Sexo deve ser 'Mascilino' ou 'Feminino'"
                                )
        
        if not gravadora_id or not isinstance(gravadora_id, int):
            raise ErrorResponse(400,
                                "gravadora_id inválido"
                                )
        
        if not feat_id or not isinstance(feat_id, int):
            raise ErrorResponse(400,
                                "feat_id inválido"
                                )
        
        # Cria objeto Cantor populado
        cantorAtualizado = Cantor(
            id=idCantor,
            nomeCantor=nomeCantor,
            nacionalidade=nacionalidade,
            idade=idade,
            sexo=sexo,
            gravadora_id=gravadora_id,
            feat_id=feat_id
        )
        
        print("✅ CantorService.updateCantor()")
        sucesso = self.daoCantorDependency.update(cantorAtualizado)
        
        if not sucesso:
            raise ErrorResponse(500,
                                "Falha ao atualizar cantor"
                                )  
        return sucesso
    
    
    # Delete
    def deleteCantor(self, idCantor: int) -> bool:
        
        # Verifica se existe
        cantor = self.daoCantorDependency.findById(idCantor)
        if not cantor:
            raise ErrorResponse(404,
                                "Cantor não encontrado",
                                {"id": idCantor}
                                )
        
        sucesso = self.daoCantorDependency.delete(idCantor)
        
        if not sucesso:
            raise ErrorResponse(500,
                                "Falha ao deletar cantor"
                                )  
        
        print("✅ CantorService.deleteCantor()")
        return sucesso
    
    # Read All
    def findAllCantores(self) -> list[dict]:
        
        cantores = self.daoCantorDependency.findAll()
        
        print("✅ CantorService.findAllCantores()")
        return cantores
    
    # Read By ID
    def findCantorById(self, idCantor: int) -> dict | None:
        
        
        cantor = self.daoCantorDependency.findById(idCantor)
        
        if not cantor:
            raise ErrorResponse(404,
                                "Cantor não encontrado",
                                {"id": idCantor}
                                )
        
        print("✅ CantorService.findCantorById()")
        return cantor