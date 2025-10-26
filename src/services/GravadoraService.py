from src.models.Gravadora import Gravadora
from src.dao.GravadoraDAO import GravadoraDAO
from src.utils.ErrorResponse import ErrorResponse

class GravadoraService:
    
    def __init__(self, daoGravadoraDependency: GravadoraDAO):
        self.daoGravadoraDependency = daoGravadoraDependency
        print("✅ GravadoraService initialized")
    
    
    # Create
    def createGravadora(self, gravadoraBodyRequest: dict) -> int:
        
        
        # Extrai dados do body request
        nomeGravadora = gravadoraBodyRequest.get("nomeGravadora")
        localizacao = gravadoraBodyRequest.get("localizacao")
        
        # Validações
        if not nomeGravadora or len(nomeGravadora) < 2:
            raise ErrorResponse(400,
                                "Nome da gravadora deve ter pelo menos 2 caracteres")
        
        if not localizacao or len(localizacao) < 2:
            raise ErrorResponse(400,
                                "Localização deve ter pelo menos 2 caracteres")
        
        # Verifica se gravadora já existe
        gravadoraExistente = self.daoGravadoraDependency.findByField('nomeGravadora', nomeGravadora)
        if gravadoraExistente and len(gravadoraExistente) > 0:
            raise ErrorResponse(400,
                                "Já existe uma gravadora com esse nome",
                                {"nomeGravadora": nomeGravadora})
        
        # Cria objeto Gravadora populado
        gravadora = Gravadora(
            nomeGravadora=nomeGravadora,
            localizacao=localizacao
        )
        
        print("✅ GravadoraService.createGravadora()")
        return self.daoGravadoraDependency.create(gravadora)
    
    
    # Update
    def updateGravadora(self, gravadoraBodyRequest: dict, idGravadora: int) -> bool:
        
        
        # Busca gravadora existente
        gravadoraExistente = self.daoGravadoraDependency.findById(idGravadora)
        if not gravadoraExistente:
            raise ErrorResponse(404,
                                "Gravadora não encontrada",
                                {"id": idGravadora})
        
        # Pega dados novos ou mantém antigos (atualização parcial)
        nomeGravadora = gravadoraBodyRequest.get("nomeGravadora", gravadoraExistente['nomeGravadora'])
        localizacao = gravadoraBodyRequest.get("localizacao", gravadoraExistente['localizacao'])
        
        # Validações
        if not nomeGravadora or len(nomeGravadora) < 2:
            raise ErrorResponse(400,
                                "Nome da gravadora deve ter pelo menos 2 caracteres")
        
        if not localizacao or len(localizacao) < 2:
            raise ErrorResponse(400,
                                "Localização deve ter pelo menos 2 caracteres")
        
        # Verifica se nome já existe em outra gravadora
        if nomeGravadora != gravadoraExistente['nomeGravadora']:
            gravadora_com_nome = self.daoGravadoraDependency.findByField('nomeGravadora', nomeGravadora)
            if gravadora_com_nome and gravadora_com_nome[0]['idGravadora'] != idGravadora:
                raise ErrorResponse(400,
                                    "Já existe uma gravadora com esse nome")
        
        # Cria objeto Gravadora atualizado
        gravadoraAtualizada = Gravadora(
            nomeGravadora=nomeGravadora,
            localizacao=localizacao,
            id=idGravadora
        )
        
        # Atualiza no banco
        sucesso = self.daoGravadoraDependency.update(gravadoraAtualizada)
        
        if not sucesso:
            raise ErrorResponse(500,
                                "Falha ao atualizar gravadora")
        
        print("✅ GravadoraService.updateGravadora()")
        return sucesso
    
    
    # Delete
    def deleteGravadora(self, idGravadora: int) -> bool:
        
        
        # Verifica se existe
        gravadora = self.daoGravadoraDependency.findById(idGravadora)
        if not gravadora:
            raise ErrorResponse(404,
                                "Gravadora não encontrada",
                                {"id": idGravadora})
        
        sucesso = self.daoGravadoraDependency.delete(idGravadora)
        
        if not sucesso:
            raise ErrorResponse(500,
                                "Falha ao deletar gravadora")
        
        print("✅ GravadoraService.deleteGravadora()")
        return sucesso
    
    
    # Read All
    def findAllGravadoras(self) -> list[dict]:
        
        
        gravadoras = self.daoGravadoraDependency.findAll()
        
        print(f"✅ GravadoraService.findAllGravadoras() -> {len(gravadoras)} registros")
        return gravadoras
    
    
    # Read By ID
    def findGravadoraById(self, idGravadora: int) -> dict | None:
        
        
        gravadora = self.daoGravadoraDependency.findById(idGravadora)
        
        if not gravadora:
            raise ErrorResponse(404,
                                "Gravadora não encontrada",
                                {"id": idGravadora})
        
        print("✅ GravadoraService.findGravadoraById()")
        return gravadora