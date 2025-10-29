from src.models.Gravadora import Gravadora
from src.dao.GravadoraDAO import GravadoraDAO
from src.utils.ErrorResponse import ErrorResponse

class GravadoraService:
    def __init__(self, daoGravadoraDependency: GravadoraDAO):
        self.daoGravadoraDependency = daoGravadoraDependency
        print("✅ GravadoraService initialized")
    
    def createGravadora(self, gravadoraBodyRequest: dict) -> int:
        # Extrai dados do body
        nomeGravadora = gravadoraBodyRequest.get("nomeGravadora")
        localizacao = gravadoraBodyRequest.get("localizacao")
        
        # Validações
        if not nomeGravadora or len(nomeGravadora) < 2:
            raise ErrorResponse(400, "Nome da gravadora deve ter pelo menos 2 caracteres")
        
        if not localizacao or len(localizacao) < 2:
            raise ErrorResponse(400, "Localização deve ter pelo menos 2 caracteres")
        
        # Cria objeto Gravadora - ✅ ORDEM CORRETA
        gravadora = Gravadora(
            nomeGravadora=nomeGravadora,
            localizacao=localizacao
            # idGravadora não precisa (é None por padrão)
        )
        
        print("✅ GravadoraService.createGravadora()")
        return self.daoGravadoraDependency.create(gravadora)
    
    def updateGravadora(self, gravadoraBodyRequest: dict, idGravadora: int) -> bool:
        # Busca gravadora existente
        gravadora_existente = self.daoGravadoraDependency.findById(idGravadora)
        
        if not gravadora_existente:
            raise ErrorResponse(404, "Gravadora não encontrada", {"id": idGravadora})
        
        # Pega dados novos ou mantém antigos
        nomeGravadora = gravadoraBodyRequest.get("nomeGravadora", gravadora_existente['nomeGravadora'])
        localizacao = gravadoraBodyRequest.get("localizacao", gravadora_existente['localizacao'])
        
        # Validações
        if len(nomeGravadora) < 2:
            raise ErrorResponse(400, "Nome da gravadora deve ter pelo menos 2 caracteres")
        
        if len(localizacao) < 2:
            raise ErrorResponse(400, "Localização deve ter pelo menos 2 caracteres")
        
        # Cria objeto Gravadora atualizado - ✅ ORDEM CORRETA
        gravadora = Gravadora(
            nomeGravadora=nomeGravadora,
            localizacao=localizacao,
            idGravadora=idGravadora  # ✅ Passa o ID para update
        )
        
        sucesso = self.daoGravadoraDependency.update(gravadora)
        
        if not sucesso:
            raise ErrorResponse(500, "Falha ao atualizar gravadora")
        
        print("✅ GravadoraService.updateGravadora()")
        return sucesso
    
    def deleteGravadora(self, idGravadora: int) -> bool:
        gravadora = self.daoGravadoraDependency.findById(idGravadora)
        if not gravadora:
            raise ErrorResponse(404, "Gravadora não encontrada", {"id": idGravadora})
        
        sucesso = self.daoGravadoraDependency.delete(idGravadora)
        print("✅ GravadoraService.deleteGravadora()")
        return sucesso
    
    def findAll(self) -> list[dict]:
        gravadoras = self.daoGravadoraDependency.findAll()
        print(f"✅ GravadoraService.findAll() -> {len(gravadoras)} registros")
        return gravadoras
    
    def findById(self, idGravadora: int) -> dict | None:
        gravadora = self.daoGravadoraDependency.findById(idGravadora)
        
        if not gravadora:
            raise ErrorResponse(404, "Gravadora não encontrada", {"id": idGravadora})
        
        print("✅ GravadoraService.findById()")
        return gravadora