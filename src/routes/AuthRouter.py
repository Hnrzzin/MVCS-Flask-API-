from flask import Blueprint, request
# Agrupa rotas relacionadas (todas de Cantor ficam juntas)
# Por que Blueprint? Separa rotas de Cantores, Usuário, Gravadora, etc. Cada entidade tem seu próprio "módulo" de rotas.
from src.utils.jwtHelper import token_required
from src.middlewares.UsuarioMiddleware import UserMiddleware
from src.controlles.UsuarioController import UsuarioController

class AuthRouter:
    
    def __init__(self, usermiddleware: UserMiddleware, usercontroller: UsuarioController):
        self.usermiddleware = usermiddleware
        self.usercontroller = usercontroller
        # Blueprint é a coleção de rotas da entidade User
        self.blueprint = Blueprint('Usuario', __name__)
        print ("⬆️ RouterAuth.contructor()")
        
    def createRoutes(self):
        """
        Configura e retorna todas as rotas REST da entidade do Usuario.

        Rotas implementadas:
        - POST /        -> Cria um novo cargo
        - GET /         -> Lista todos os cargos
        - GET /<id>     -> Retorna um cargo por ID
        - PUT /<id>     -> Atualiza um cargo por ID
        - DELETE /<id>  -> Remove um cargo por ID

        Observações:
        - Middlewares de validação são aplicados diretamente.
        """
        
        @self.blueprint.route('/cadastro', methods = ['POST'])
        @self.usermiddleware.validateBody
        
        def store():
            return self.usercontroller.store()
        
        @self.blueprint.route('/login', methods = ['POST'])
        @token_required
        @self.usermiddleware.validateBody
        
        def store():
            return self.usercontroller.store()
        
        
        
        @self.blueprint.route('/users', methods = ['GET'])
        
        def index():
            return self.usercontroller.index()
        
        @self.blueprint.route('/users/<int:idUsuario>', methods = ['GET'])
        @self.usermiddleware.validateIdParam
        
        def show(idUsuario):
            return self.usercontroller.show()
        
        @self.blueprint.route('/users/<int:idUsuario>', methods = ['PUT'])
        @self.usermiddleware.validateBody
        @self.usermiddleware.validateIdParam
        
        def update(idUsuario):
            return self.usercontroller.update()
        
        @self.blueprint.route('/disconnect/<int:idUsuario>', methods = ['DELETE'])
        @self.usermiddleware.validateIdParam
        
        def destroy(idUsuario):
            return self.usercontroller.destroy()
        
        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.blueprint
        
        
        
    