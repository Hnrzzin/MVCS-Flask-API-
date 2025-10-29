from flask import request, jsonify
from src.services.CantorService import CantorService
from src.utils.ErrorResponse import ErrorResponse

class CantorController:
    
    def __init__(self, cantor_service: CantorService):
        print("✅ CantorController initialized")
        self.__cantor_service = cantor_service
    
    
    # CREATE - Cria um novo cantor
    def store(self):
        
        print("🔵 CantorController.store()")
        
        cantorBodyRequest = request.json
        
        # Service valida e cria
        novo_id = self.__cantor_service.createCantor(cantorBodyRequest)
        
        return jsonify({
            "success": True,
            "message": "Cantor criado com sucesso",
            "data": {
                "idCantor": novo_id,
                "nomeCantor": cantorBodyRequest.get("nomeCantor"),
                "nacionalidade": cantorBodyRequest.get("nacionalidade")
            }
        }), 201
    
    
    # READ ALL - Lista todos os cantores
    def index(self):
        
        print("🔵 CantorController.index()")
        
        allCantores = self.__cantor_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Cantores listados com sucesso",
            "data": {
                "cantores": allCantores
            }
        }), 200
    
    
    # READ ONE - Busca cantor por ID
    def show(self, idCantor):
        
        print("🔵 CantorController.show()")
        
        # Service lança ErrorResponse 404 se não encontrar
        cantor = self.__cantor_service.findById(int(idCantor))
        
        return jsonify({
            "success": True,
            "message": "Cantor encontrado",
            "data": {
                "cantor": cantor
            }
        }), 200
    
    
    # UPDATE - Atualiza cantor existente
    def update(self, idCantor):
        """Atualiza um cantor existente"""
        print("🔵 CantorController.update()")
        
        # Pega ID da URL
        
        
        # Pega dados do body
        cantorBodyRequest = request.json
        
        # Service valida e atualiza
        self.__cantor_service.updateCantor(cantorBodyRequest, int(idCantor))
        
        return jsonify({
            "success": True,
            "message": "Cantor atualizado com sucesso",
            "data": {
                "idCantor": int(idCantor),
                "nomeCantor": cantorBodyRequest.get("nomeCantor"),
                "nacionalidade": cantorBodyRequest.get("nacionalidade")
            }
        }), 200
    
    
    # DELETE - Remove cantor
    def destroy(self, idCantor):
        """Remove um cantor pelo ID"""
        print("🔵 CantorController.destroy()")
        
        
        
        # Service valida e deleta
        self.__cantor_service.deleteCantor(int(idCantor))
        
        return jsonify({
            "success": True,
            "message": "Cantor excluído com sucesso"
        }), 200