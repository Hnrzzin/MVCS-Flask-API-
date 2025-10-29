from src.models.FeatFamoso import FeatFamoso
from src.dao.FeatFamosoDAO import FeatFamosoDAO
from src.utils.ErrorResponse import ErrorResponse

class FeatFamosoService:
    def __init__(self, daoFeatDependency: FeatFamosoDAO):
        self.daoFeatDependency = daoFeatDependency
        print("✅ FeatFamosoService initialized")
    
    def createFeat(self, featBodyRequest: dict) -> int:
        # Extrai dados do body
        nomeFeat = featBodyRequest.get("nomeFeat")
        cantorFeat = featBodyRequest.get("cantorFeat")
        streams = featBodyRequest.get("streams")
        
        # Validações
        if not nomeFeat or len(nomeFeat) < 2:
            raise ErrorResponse(400, "Nome do feat deve ter pelo menos 2 caracteres")
        
        if not cantorFeat or len(cantorFeat) < 2:
            raise ErrorResponse(400, "Nome do cantor deve ter pelo menos 2 caracteres")
        
        if not streams:
            raise ErrorResponse(400, "Streams é obrigatório")
        
        # Cria objeto FeatFamoso - ✅ ORDEM CORRETA
        feat = FeatFamoso(
            nomeFeat=nomeFeat,
            cantorFeat=cantorFeat,
            streams=streams
            # idFeat não precisa (é None por padrão)
        )
        
        print("✅ FeatFamosoService.createFeat()")
        return self.daoFeatDependency.create(feat)
    
    def updateFeat(self, featBodyRequest: dict, idFeat: int) -> bool:
        # Busca feat existente
        feat_existente = self.daoFeatDependency.findById(idFeat)
        
        if not feat_existente:
            raise ErrorResponse(404, "Feat não encontrado", {"id": idFeat})
        
        # Pega dados novos ou mantém antigos
        nomeFeat = featBodyRequest.get("nomeFeat", feat_existente['nomeFeat'])
        cantorFeat = featBodyRequest.get("cantorFeat", feat_existente['cantorFeat'])
        streams = featBodyRequest.get("streams", feat_existente['streams'])
        
        # Validações
        if len(nomeFeat) < 2:
            raise ErrorResponse(400, "Nome do feat deve ter pelo menos 2 caracteres")
        
        if len(cantorFeat) < 2:
            raise ErrorResponse(400, "Nome do cantor deve ter pelo menos 2 caracteres")
        
        # Cria objeto FeatFamoso atualizado - ✅ ORDEM CORRETA
        feat = FeatFamoso(
            nomeFeat=nomeFeat,
            cantorFeat=cantorFeat,
            streams=streams,
            idFeat=idFeat  # ✅ Passa o ID para update
        )
        
        sucesso = self.daoFeatDependency.update(feat)
        
        if not sucesso:
            raise ErrorResponse(500, "Falha ao atualizar feat")
        
        print("✅ FeatFamosoService.updateFeat()")
        return sucesso
    
    def deleteFeat(self, idFeat: int) -> bool:
        feat = self.daoFeatDependency.findById(idFeat)
        if not feat:
            raise ErrorResponse(404, "Feat não encontrado", {"id": idFeat})
        
        sucesso = self.daoFeatDependency.delete(idFeat)
        print("✅ FeatFamosoService.deleteFeat()")
        return sucesso
    
    def findAll(self) -> list[dict]:
        feats = self.daoFeatDependency.findAll()
        print(f"✅ FeatFamosoService.findAll() -> {len(feats)} registros")
        return feats
    
    def findById(self, idFeat: int) -> dict | None:
        feat = self.daoFeatDependency.findById(idFeat)
        
        if not feat:
            raise ErrorResponse(404, "Feat não encontrado", {"id": idFeat})
        
        print("✅ FeatFamosoService.findById()")
        return feat