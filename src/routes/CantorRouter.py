from flask import Blueprint, request
# Agrupa rotas relacionadas (todas de Cantor ficam juntas)
# Por que Blueprint? Separa rotas de Cantores, Usuário, Gravadora, etc. Cada entidade tem seu próprio "módulo" de rotas.
from src.utils.jwtHelper import token_required
from src.middlewares.CantorMiddleware import CantorMiddleware
from src.controlles.CantorController import CantorController

class CantorRouter:
    
    def __init__(self, cantormiddleware: CantorMiddleware, cantorcontroller: CantorController):
        self.cantormiddleware = cantormiddleware
        self.cantorcontroller = cantorcontroller
        # Blueprint é a coleção de rotas da entidade User
        self.blueprint = Blueprint('Cantor', __name__)
        print ("⬆️ RouterCantor.contructor()")
        
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
        
        @self.blueprint.route('/cantores', methods = ['POST'])
        @token_required
        
        @self.cantormiddleware.validateBody
        
        def store():
            return self.cantorcontroller.store()
        
    
        @self.blueprint.route('/cantores', methods = ['GET'])
        
        def index():
            return self.cantorcontroller.index()
        
        @self.blueprint.route('/cantores/<int:idCantor>', methods = ['GET'])
        @token_required
        @self.cantormiddleware.validateIdParam
        
        def show(idCantor):
            return self.cantorcontroller.show()
        
        @self.blueprint.route('/cantores/<int:idCantor>', methods = ['PUT'])
        @token_required
        @self.cantormiddleware.validateBody
        @self.cantormiddleware.validateIdParam
        
        def update(idCantor):
            return self.cantorcontroller.update()
        
        @self.blueprint.route('/disconnect/<int:idCantor>', methods = ['DELETE'])
        @token_required
        @self.cantormiddleware.validateIdParam
        
        def destroy(idCantor):
            return self.cantorcontroller.destroy()
        
        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.blueprint