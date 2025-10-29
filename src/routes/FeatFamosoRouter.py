from flask import Blueprint
from src.utils.jwtHelper import token_required
from src.middlewares.FeatFamosoMiddleware import FeatFamosoMiddleware
from src.controlles.FeatFamosoController import FeatFamosoController

class FeatFamosoRouter:
    """Router para todas as rotas de FeatFamoso"""
    
    def __init__(self, featmiddleware: FeatFamosoMiddleware, featcontroller: FeatFamosoController):
        self.featmiddleware = featmiddleware
        self.featcontroller = featcontroller
        self.blueprint = Blueprint('FeatFamoso', __name__)
        print("⬆️ FeatFamosoRouter.constructor()")
        
    def createRoutes(self):
        """
        Configura todas as rotas REST de FeatFamoso
        
        Rotas:
        - POST   /feats          -> Cria novo feat
        - GET    /feats          -> Lista todos feats
        - GET    /feats/<id>     -> Busca feat por ID
        - PUT    /feats/<id>     -> Atualiza feat
        - DELETE /feats/<id>     -> Remove feat
        """
        
        # CREATE - Criar novo feat
        @self.blueprint.route('/feats', methods=['POST'])
        @token_required
        @self.featmiddleware.validateBody
        def store():
            return self.featcontroller.store()
        
        
        # READ ALL - Listar todos feats
        @self.blueprint.route('/feats', methods=['GET'])
        @token_required
        def index():
            return self.featcontroller.index()
        
        
        # READ ONE - Buscar feat por ID
        @self.blueprint.route('/feats/<int:idFeat>', methods=['GET'])
        @token_required
        @self.featmiddleware.validateIdParam
        def show(idFeat):
            return self.featcontroller.show()
        
        
        # UPDATE - Atualizar feat
        @self.blueprint.route('/feats/<int:idFeat>', methods=['PUT'])
        @token_required
        @self.featmiddleware.validateIdParam
        @self.featmiddleware.validateBody
        def update(idFeat):
            return self.featcontroller.update()
        
        
        # DELETE - Remover feat
        @self.blueprint.route('/feats/<int:idFeat>', methods=['DELETE'])
        @token_required
        @self.featmiddleware.validateIdParam
        def destroy(idFeat):
            return self.featcontroller.destroy()
        
        
        return self.blueprint
