from flask import Blueprint, request
# Agrupa rotas relacionadas (todas de Cantor ficam juntas)
# Por que Blueprint? Separa rotas de Cantores, Usuário, Gravadora, etc. Cada entidade tem seu próprio "módulo" de rotas.
from src.middlewares.UsuarioMiddleware import UserMiddleware
from src.controlles.UsuarioController import UsuarioController
from src.utils.jwtHelper import token_required

class AuthRouter:
    def __init__(self, usermiddleware: UserMiddleware, usercontroller: UsuarioController):
        self.usermiddleware = usermiddleware
        self.usercontroller = usercontroller
        self.blueprint = Blueprint('Usuario', __name__)
        print("⬆️ RouterAuth.contructor()")
        
    def createRoutes(self):
        # CADASTRO (público)
        @self.blueprint.route('/cadastro', methods=['POST'])
        @self.usermiddleware.validateBody
        def register():  # ✅ Nome único
            return self.usercontroller.store()
        
        # LOGIN (público - SEM token_required)
        @self.blueprint.route('/login', methods=['POST'])
        @self.usermiddleware.validateBody
        def login():  # ✅ Nome único e método correto
            return self.usercontroller.login()
        
        # LISTAR (protegido)
        @self.blueprint.route('/users', methods=['GET'])
        @token_required
        def index():
            return self.usercontroller.index()
        
        # BUSCAR (protegido)
        @self.blueprint.route('/users/<int:idUsuario>', methods=['GET'])
        @token_required
        @self.usermiddleware.validateIdParam
        def show(idUsuario):
            return self.usercontroller.show(idUsuario)
        
        # ATUALIZAR (protegido)
        @self.blueprint.route('/users/<int:idUsuario>', methods=['PUT'])
        @token_required
        @self.usermiddleware.validateBody
        @self.usermiddleware.validateIdParam
        def update(idUsuario):
            return self.usercontroller.update(idUsuario)
        
        # DELETAR (protegido)
        @self.blueprint.route('/disconnect/<int:idUsuario>', methods=['DELETE'])
        @token_required
        @self.usermiddleware.validateIdParam
        def destroy(idUsuario):
            return self.usercontroller.destroy(idUsuario)
        
        return self.blueprint



        
    