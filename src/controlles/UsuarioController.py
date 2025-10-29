from src.services.UsuarioService import UsuarioService
from flask import jsonify, request
from src.utils.ErrorResponse import ErrorResponse
from src.utils.jwtHelper import gerar_token

class UsuarioController:
    def __init__(self, userService: UsuarioService):
        print("✅ UsuarioController initialized")
        self.userService = userService
        

    
    # CREATE - Cria um novo usuário
    def store(self):
        
        print("🔵 UsuarioController.store()")
        
        userBodyRequest = request.json
        
        # Service valida e cria
        novo_id = self.userService.createUser(userBodyRequest)
        novo_token = gerar_token(
                                userBodyRequest.get('email'),
                                userBodyRequest.get('senha')
                            )
        
        return jsonify({
            "success": True,
            "message": "Usuário criado com sucesso",
            "data": {
                "idUsuario": novo_id,
                "nome": userBodyRequest.get("nome"),
                "email": userBodyRequest.get("email"),
                "token": f'{novo_token}'
            }
        }), 201
    
    
    # READ ALL - Lista todos os usuários
    def index(self):
        
        print("🔵 UsuarioController.index()")
        
        allUsers = self.userService.findAll()
        
        
        return jsonify({
            "success": True,
            "message": "Usuários listados com sucesso",
            "data": {
                "usuarios": allUsers
            }
        }), 200  
    
    
    # READ ONE - Busca usuário por ID
    def show(self):
        
        print("🔵 UsuarioController.show()")
        
        idUsuario = request.view_args.get("idUsuario")
        
        # Service lança ErrorResponse 404 se não encontrar
        usuario = self.userService.findById(int(idUsuario))
        
        return jsonify({
            "success": True,
            "message": "Usuário encontrado",
            "data": {
                "usuario": usuario  
            }
        }), 200
    
    
    # UPDATE - Atualiza usuário existente
    def update(self):
        
        print("🔵 UsuarioController.update()")
        
        # Pega ID da URL
        idUsuario = request.view_args.get("idUsuario")
        
        # Pega dados do body
        userBodyRequest = request.json
        
        # Service valida e atualiza (lança ErrorResponse se falhar)
        self.userService.updateUser(userBodyRequest, int(idUsuario))
        
        # Retorna sucesso (não precisa buscar novamente)
        return jsonify({
            "success": True,
            "message": "Usuário atualizado com sucesso",
            "data": {
                "idUsuario": int(idUsuario),
                "nome": userBodyRequest.get("nome"),
                "email": userBodyRequest.get("email")
                
            }
        }), 200
    
    
    # DELETE - Remove usuário
    def destroy(self):
        
        print("🔵 UsuarioController.destroy()")
        
        # Pega ID da URL
        idUsuario = request.view_args.get("idUsuario")
        
        # Service valida e deleta (lança ErrorResponse se não existir)
        self.userService.deleteUser(int(idUsuario))
        
        # Retorna sucesso
        return jsonify({
            "success": True,
            "message": "Usuário excluído com sucesso"
        }), 200  # ou 204 No Content (sem body)