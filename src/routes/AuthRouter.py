# Agrupa rotas relacionadas (todas de Cantor ficam juntas)
# Por que Blueprint? Separa rotas de Cantores, Usuário, Gravadora, etc. Cada entidade tem seu próprio "módulo" de rotas.
from flask import Blueprint, request
from src.middlewares.UsuarioMiddleware import UsuarioMiddleware
from src.controlles.UsuarioController import UsuarioController  
from src.utils.jwtHelper import token_required

class AuthRouter:
    def __init__(self, usermiddleware: UsuarioMiddleware, usercontroller: UsuarioController):
        self.usermiddleware = usermiddleware
        self.usercontroller = usercontroller
        self.blueprint = Blueprint('Usuario', __name__)
        print("⬆️ RouterAuth.constructor()")
        
    def createRoutes(self):
        # CADASTRO (público)
        @self.blueprint.route('/cadastro', methods=['POST'])
        @self.usermiddleware.validar_body_create  
        def register():
            return self.usercontroller.store()
        
        # LOGIN (público - SEM token_required)
        @self.blueprint.route('/login', methods=['POST'])
        @self.usermiddleware.validar_body_login  
        def login():
            return self.usercontroller.login()
        
        # LISTAR (protegido)
        @self.blueprint.route('/users', methods=['GET'])
        @token_required
        def index():
            return self.usercontroller.index()
        
        # BUSCAR (protegido)
        @self.blueprint.route('/users/<int:idUsuario>', methods=['GET'])
        @token_required
        @self.usermiddleware.validar_id_usuario  
        def show(idUsuario):
            return self.usercontroller.show(idUsuario)
        
        # ATUALIZAR (protegido)
        @self.blueprint.route('/users/<int:idUsuario>', methods=['PUT'])
        @token_required
        @self.usermiddleware.validar_id_usuario  
        @self.usermiddleware.validar_body_update  
        def update(idUsuario):
            return self.usercontroller.update(idUsuario)
        
        # DELETAR (protegido)
        @self.blueprint.route('/disconnect/<int:idUsuario>', methods=['DELETE'])
        @token_required
        @self.usermiddleware.validar_id_usuario  
        def destroy(idUsuario):
            return self.usercontroller.destroy(idUsuario)
        
        return self.blueprint

        
    
    
