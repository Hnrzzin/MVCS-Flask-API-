from flask import Blueprint
from src.utils.jwtHelper import token_required
from src.middlewares.FeatFamosoMiddleware import FeatFamosoMiddleware
from src.controlles.FeatFamosoController import FeatFamosoController

class FeatFamosoRouter:
    
    def __init__(self, featmiddleware: FeatFamosoMiddleware, featcontroller: FeatFamosoController):
        self.featmiddleware = featmiddleware
        self.featcontroller = featcontroller
        self.blueprint = Blueprint('FeatFamoso', __name__)
        print("⬆️ FeatFamosoRouter.constructor()")
        
    def createRoutes(self):
        # CREATE
        @self.blueprint.route('/feats', methods=['POST'], endpoint='create_feat')
        @token_required
        @self.featmiddleware.validateBody
        def store():
            return self.featcontroller.store()
        
        # READ ALL
        @self.blueprint.route('/feats', methods=['GET'], endpoint='list_feats')
        @token_required
        def index():
            return self.featcontroller.index()
        
        # READ ONE
        @self.blueprint.route('/feats/<int:idFeat>', methods=['GET'], endpoint='show_feat')
        @token_required
        @self.featmiddleware.validateIdParam
        def show(idFeat):
            return self.featcontroller.show(idFeat)  # ✅ Passa o ID
        
        # UPDATE
        @self.blueprint.route('/feats/<int:idFeat>', methods=['PUT'], endpoint='update_feat')
        @token_required
        @self.featmiddleware.validateIdParam
        @self.featmiddleware.validateBody
        def update(idFeat):
            return self.featcontroller.update(idFeat)  # ✅ Passa o ID
        
        # DELETE
        @self.blueprint.route('/feats/<int:idFeat>', methods=['DELETE'], endpoint='delete_feat')
        @token_required
        @self.featmiddleware.validateIdParam
        def destroy(idFeat):
            return self.featcontroller.destroy(idFeat)  # ✅ Passa o ID
        
        return self.blueprint