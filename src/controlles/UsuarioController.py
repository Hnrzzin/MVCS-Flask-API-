from src.services.UsuarioService import UsuarioService
from flask import jsonify, request
from src.utils.ErrorResponse import ErrorResponse
from src.utils.jwtHelper import gerar_token, token_required

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
    
        
        return jsonify({
            "success": True,
            "message": "Usuário criado com sucesso",
            "data": {
                "idUsuario": novo_id,
                "nome": userBodyRequest.get("nome"),
                "email": userBodyRequest.get("email")
            
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
    def show(self, idUsuario):  # ✅ Já recebe o parâmetro
        
        print("🔵 UsuarioController.show()")
        
        # O Flask já passa como argumento
        
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
    def update(self, idUsuario):
        
        print("🔵 UsuarioController.update()")
        
        userBodyRequest = request.json
        self.userService.updateUser(userBodyRequest, int(idUsuario))
    
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
    def destroy(self, idUsuario):
        
        print("🔵 UsuarioController.destroy()")
        
        # Service valida e deleta (lança ErrorResponse se não existir)
        sucesso = self.userService.deleteUser(int(idUsuario))
        if sucesso == True:
            # Retorna sucesso
            return jsonify({
                "success": True,
                "message": "Usuário excluído com sucesso"
            }), 200  # ou 204 No Content (sem body)
        
    def login(self):
        """LOGIN - Autentica usuário e retorna token"""
        
        print("🔵 UsuarioController.login()")
        
        userBodyRequest = request.json
        email = userBodyRequest.get('email')
        senha = userBodyRequest.get('senha')
        
        # Valida presença de campos
        if not email or not senha:
            raise ErrorResponse(400, "Email e senha são obrigatórios")
        
        # Service autentica
        usuario = self.userService.authenticateUser(email, senha)
        
        # Gera token
        token = gerar_token(usuario['idUsuario'], usuario['email'])
        
        return jsonify({
            "success": True,
            "message": "Login realizado com sucesso",
            "data": {
                "usuario": usuario,
                "token": token
            }
        }), 200