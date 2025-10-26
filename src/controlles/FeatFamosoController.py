from flask import request, jsonify
from src.services.FeatFamosoService import FeatFamosoService
from src.utils.ErrorResponse import ErrorResponse

class FeatFamosoController:
    
    def __init__(self, feat_service: FeatFamosoService):
        print("✅ FeatFamosoController initialized")
        self.__feat_service = feat_service
    
    
    # CREATE - Cria um novo feat
    def store(self):
        """Cria um novo feat famoso"""
        print("🔵 FeatFamosoController.store()")
        
        featBodyRequest = request.json
        
        # Service valida e cria
        novo_id = self.__feat_service.createFeat(featBodyRequest)
        
        return jsonify({
            "success": True,
            "message": "Feat criado com sucesso",
            "data": {
                "idFeat": novo_id,
                "nomeFeat": featBodyRequest.get("nomeFeat"),
                "cantorFeat": featBodyRequest.get("cantorFeat"),
                "streams": featBodyRequest.get("streams")
            }
        }), 201
    
    
    # READ ALL - Lista todos os feats
    def index(self):
        """Lista todos os feats famosos"""
        print("🔵 FeatFamosoController.index()")
        
        allFeats = self.__feat_service.findAllFeats()
        
        return jsonify({
            "success": True,
            "message": "Feats listados com sucesso",
            "data": {
                "feats": allFeats
            }
        }), 200
    
    
    # READ ONE - Busca feat por ID
    def show(self):
        """Busca feat por ID"""
        print("🔵 FeatFamosoController.show()")
        
        idFeat = request.view_args.get("idFeat")
        
        # Service lança ErrorResponse 404 se não encontrar
        feat = self.__feat_service.findFeatById(int(idFeat))
        
        return jsonify({
            "success": True,
            "message": "Feat encontrado",
            "data": {
                "feat": feat
            }
        }), 200
    
    
    # UPDATE - Atualiza feat existente
    def update(self):
        """Atualiza um feat existente"""
        print("🔵 FeatFamosoController.update()")
        
        # Pega ID da URL
        idFeat = request.view_args.get("idFeat")
        
        # Pega dados do body
        featBodyRequest = request.json
        
        # Service valida e atualiza
        self.__feat_service.updateFeat(featBodyRequest, int(idFeat))
        
        return jsonify({
            "success": True,
            "message": "Feat atualizado com sucesso",
            "data": {
                "idFeat": int(idFeat),
                "nomeFeat": featBodyRequest.get("nomeFeat"),
                "cantorFeat": featBodyRequest.get("cantorFeat"),
                "streams": featBodyRequest.get("streams")
            }
        }), 200
    
    
    # DELETE - Remove feat
    def destroy(self):
        """Remove um feat pelo ID"""
        print("🔵 FeatFamosoController.destroy()")
        
        idFeat = request.view_args.get("idFeat")
        
        # Service valida e deleta
        self.__feat_service.deleteFeat(int(idFeat))
        
        return jsonify({
            "success": True,
            "message": "Feat excluído com sucesso"
        }), 200