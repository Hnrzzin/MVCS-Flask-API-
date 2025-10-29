from flask import Blueprint
from src.utils.jwtHelper import token_required
from src.middlewares.GravadoraMiddleware import GravadoraMiddleware
from src.controlles.GravadoraController import GravadoraController  # ✅ CORRIGIDO

class GravadoraRouter:
    
    def __init__(self, gravadoramiddleware: GravadoraMiddleware, gravadoracontroller: GravadoraController):
        self.gravadoramiddleware = gravadoramiddleware
        self.gravadoracontroller = gravadoracontroller
        self.blueprint = Blueprint('Gravadora', __name__)
        print("⬆️ GravadoraRouter.constructor()")
        
    def createRoutes(self):
        # CREATE
        @self.blueprint.route('/gravadoras', methods=['POST'], endpoint='create_gravadora')
        @token_required
        @self.gravadoramiddleware.validar_body_create  # ✅ CORRIGIDO
        def store():
            return self.gravadoracontroller.store()
        
        # READ ALL
        @self.blueprint.route('/gravadoras', methods=['GET'], endpoint='list_gravadoras')
        @token_required
        def index():
            return self.gravadoracontroller.index()
        
        # READ ONE
        @self.blueprint.route('/gravadoras/<int:idGravadora>', methods=['GET'], endpoint='show_gravadora')
        @token_required
        @self.gravadoramiddleware.validar_id_gravadora  # ✅ CORRIGIDO
        def show(idGravadora):
            return self.gravadoracontroller.show(idGravadora)
        
        # UPDATE
        @self.blueprint.route('/gravadoras/<int:idGravadora>', methods=['PUT'], endpoint='update_gravadora')
        @token_required
        @self.gravadoramiddleware.validar_id_gravadora  # ✅ CORRIGIDO
        @self.gravadoramiddleware.validar_body_update  # ✅ CORRIGIDO
        def update(idGravadora):
            return self.gravadoracontroller.update(idGravadora)
        
        # DELETE
        @self.blueprint.route('/gravadoras/<int:idGravadora>', methods=['DELETE'], endpoint='delete_gravadora')
        @token_required
        @self.gravadoramiddleware.validar_id_gravadora  # ✅ CORRIGIDO
        def destroy(idGravadora):
            return self.gravadoracontroller.destroy(idGravadora)
        
        return self.blueprint