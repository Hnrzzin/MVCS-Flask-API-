from src.models.FeatFamoso import FeatFamoso
from src.dao.FeatFamosoDAO import FeatFamosoDAO
from src.utils.ErrorResponse import ErrorResponse

class FeatFamosoService:
    
    def __init__(self, daoFeatDependency: FeatFamosoDAO):
        self.daoFeatDependency = daoFeatDependency
        print("✅ FeatFamosoService initialized")
    
    
    # Create
    def createFeat(self, featBodyRequest: dict) -> int:
        
        
        # Extrai dados do body request
        nomeFeat = featBodyRequest.get("nomeFeat")
        cantorFeat = featBodyRequest.get("cantorFeat")
        streams = featBodyRequest.get("streams")
        
        # Validações
        if not nomeFeat or len(nomeFeat) < 2:
            raise ErrorResponse(400,
                                "Nome do feat deve ter pelo menos 2 caracteres")
        
        if not cantorFeat or len(cantorFeat) < 2:
            raise ErrorResponse(400,
                                "Nome do cantor deve ter pelo menos 2 caracteres")
        
        if not streams or not isinstance(streams, str):
            raise ErrorResponse(400,
                                "Streams deve ser uma string válida")
        
        # Cria objeto FeatFamoso populado
        feat = FeatFamoso(
            nomeFeat=nomeFeat,
            cantorFeat=cantorFeat,
            streams=streams
        )
        
        print("✅ FeatFamosoService.createFeat()")
        return self.daoFeatDependency.create(feat)
    
    
    # Update
    def updateFeat(self, featBodyRequest: dict, idFeat: int) -> bool:
        
        
        # Busca feat existente
        featExistente = self.daoFeatDependency.findById(idFeat)
        if not featExistente:
            raise ErrorResponse(404,
                                "Feat não encontrado",
                                {"id": idFeat})
        
        # Pega dados novos ou mantém antigos (atualização parcial)
        nomeFeat = featBodyRequest.get("nomeFeat", featExistente['nomeFeat'])
        cantorFeat = featBodyRequest.get("cantorFeat", featExistente['cantorFeat'])
        streams = featBodyRequest.get("streams", featExistente['streams'])
        
        # Validações
        if not nomeFeat or len(nomeFeat) < 2:
            raise ErrorResponse(400,
                                "Nome do feat deve ter pelo menos 2 caracteres")
        
        if not cantorFeat or len(cantorFeat) < 2:
            raise ErrorResponse(400,
                                "Nome do cantor deve ter pelo menos 2 caracteres")
        
        if not streams or not isinstance(streams, str):
            raise ErrorResponse(400,
                                "Streams deve ser uma string válida")
        
        # Cria objeto FeatFamoso atualizado
        featAtualizado = FeatFamoso(
            nomeFeat=nomeFeat,
            cantorFeat=cantorFeat,
            streams=streams,
            id=idFeat
        )
        
        # Atualiza no banco
        sucesso = self.daoFeatDependency.update(featAtualizado)
        
        if not sucesso:
            raise ErrorResponse(500,
                                "Falha ao atualizar feat")
        
        print("✅ FeatFamosoService.updateFeat()")
        return sucesso
    
    
    # Delete
    def deleteFeat(self, idFeat: int) -> bool:
        
        
        # Verifica se existe
        feat = self.daoFeatDependency.findById(idFeat)
        if not feat:
            raise ErrorResponse(404,
                                "Feat não encontrado",
                                {"id": idFeat})
        
        sucesso = self.daoFeatDependency.delete(idFeat)
        
        if not sucesso:
            raise ErrorResponse(500,
                                "Falha ao deletar feat")
        
        print("✅ FeatFamosoService.deleteFeat()")
        return sucesso
    
    
    # Read All
    def findAllFeats(self) -> list[dict]:
        
        
        feats = self.daoFeatDependency.findAll()
        
        print(f"✅ FeatFamosoService.findAllFeats() -> {len(feats)} registros")
        return feats
    
    
    # Read By ID
    def findFeatById(self, idFeat: int) -> dict | None:
        
        
        feat = self.daoFeatDependency.findById(idFeat)
        
        if not feat:
            raise ErrorResponse(404,
                                "Feat não encontrado",
                                {"id": idFeat})
        
        print("✅ FeatFamosoService.findFeatById()")
        return feat