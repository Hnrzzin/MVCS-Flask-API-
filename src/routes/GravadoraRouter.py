from flask import Blueprint
from src.utils.jwtHelper import token_required
from src.middlewares.GravadoraMiddleware import GravadoraMiddleware
from src.controlles.GravadoraController import GravadoraController

class GravadoraRouter:
    """Router para todas as rotas de Gravadora"""
    
    def __init__(self, gravadoramiddleware: GravadoraMiddleware, gravadoracontroller: GravadoraController):
        self.gravadoramiddleware = gravadoramiddleware
        self.gravadoracontroller = gravadoracontroller
        self.blueprint = Blueprint('Gravadora', __name__)
        print("⬆️ GravadoraRouter.constructor()")
        
    def createRoutes(self):
        """
        Configura todas as rotas REST de Gravadora
        
        Rotas:
        - POST   /gravadoras          -> Cria nova gravadora
        - GET    /gravadoras          -> Lista todas gravadoras
        - GET    /gravadoras/<id>     -> Busca gravadora por ID
        - PUT    /gravadoras/<id>     -> Atualiza gravadora
        - DELETE /gravadoras/<id>     -> Remove gravadora
        """
        
        # CREATE - Criar nova gravadora
        @self.blueprint.route('/gravadoras', methods=['POST'])
        @token_required
        @self.gravadoramiddleware.validateBody
        def store():
            return self.gravadoracontroller.store()
        
        
        # READ ALL - Listar todas gravadoras
        @self.blueprint.route('/gravadoras', methods=['GET'])
        @token_required
        def index():
            return self.gravadoracontroller.index()
        
        
        # READ ONE - Buscar gravadora por ID
        @self.blueprint.route('/gravadoras/<int:idGravadora>', methods=['GET'])
        @token_required
        @self.gravadoramiddleware.validateIdParam
        def show(idGravadora):
            return self.gravadoracontroller.show()
        
        
        # UPDATE - Atualizar gravadora
        @self.blueprint.route('/gravadoras/<int:idGravadora>', methods=['PUT'])
        @token_required
        @self.gravadoramiddleware.validateIdParam
        @self.gravadoramiddleware.validateBody
        def update(idGravadora):
            return self.gravadoracontroller.update()
        
        
        # DELETE - Remover gravadora
        @self.blueprint.route('/gravadoras/<int:idGravadora>', methods=['DELETE'])
        @token_required
        @self.gravadoramiddleware.validateIdParam
        def destroy(idGravadora):
            return self.gravadoracontroller.destroy()
        
        
        return self.blueprint