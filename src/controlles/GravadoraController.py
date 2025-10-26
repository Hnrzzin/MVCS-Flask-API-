from flask import request, jsonify
from src.services.GravadoraService import GravadoraService
from src.utils.ErrorResponse import ErrorResponse

class GravadoraController:
    
    def __init__(self, gravadora_service: GravadoraService):
        print("✅ GravadoraController initialized")
        self.__gravadora_service = gravadora_service
    
    
    # CREATE - Cria uma nova gravadora
    def store(self):
        """Cria uma nova gravadora"""
        print("🔵 GravadoraController.store()")
        
        gravadoraBodyRequest = request.json
        
        # Service valida e cria
        novo_id = self.__gravadora_service.createGravadora(gravadoraBodyRequest)
        
        return jsonify({
            "success": True,
            "message": "Gravadora criada com sucesso",
            "data": {
                "idGravadora": novo_id,
                "nomeGravadora": gravadoraBodyRequest.get("nomeGravadora"),
                "localizacao": gravadoraBodyRequest.get("localizacao")
            }
        }), 201
    
    
    # READ ALL - Lista todas as gravadoras
    def index(self):
        """Lista todas as gravadoras"""
        print("🔵 GravadoraController.index()")
        
        allGravadoras = self.__gravadora_service.findAllGravadoras()
        
        return jsonify({
            "success": True,
            "message": "Gravadoras listadas com sucesso",
            "data": {
                "gravadoras": allGravadoras
            }
        }), 200
    
    
    # READ ONE - Busca gravadora por ID
    def show(self):
        """Busca gravadora por ID"""
        print("🔵 GravadoraController.show()")
        
        idGravadora = request.view_args.get("idGravadora")
        
        # Service lança ErrorResponse 404 se não encontrar
        gravadora = self.__gravadora_service.findGravadoraById(int(idGravadora))
        
        return jsonify({
            "success": True,
            "message": "Gravadora encontrada",
            "data": {
                "gravadora": gravadora
            }
        }), 200
    
    
    # UPDATE - Atualiza gravadora existente
    def update(self):
        """Atualiza uma gravadora existente"""
        print("🔵 GravadoraController.update()")
        
        # Pega ID da URL
        idGravadora = request.view_args.get("idGravadora")
        
        # Pega dados do body
        gravadoraBodyRequest = request.json
        
        # Service valida e atualiza
        self.__gravadora_service.updateGravadora(gravadoraBodyRequest, int(idGravadora))
        
        return jsonify({
            "success": True,
            "message": "Gravadora atualizada com sucesso",
            "data": {
                "idGravadora": int(idGravadora),
                "nomeGravadora": gravadoraBodyRequest.get("nomeGravadora"),
                "localizacao": gravadoraBodyRequest.get("localizacao")
            }
        }), 200
    
    
    # DELETE - Remove gravadora
    def destroy(self):
        """Remove uma gravadora pelo ID"""
        print("🔵 GravadoraController.destroy()")
        
        idGravadora = request.view_args.get("idGravadora")
        
        # Service valida e deleta
        self.__gravadora_service.deleteGravadora(int(idGravadora))
        
        return jsonify({
            "success": True,
            "message": "Gravadora excluída com sucesso"
        }), 200