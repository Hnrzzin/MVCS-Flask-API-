from flask import Blueprint
from src.utils.jwtHelper import token_required
from src.middlewares.CantorMiddleware import CantorMiddleware
from src.controlles.CantorController import CantorController  # ✅ CORRIGIDO

class CantorRouter:
    
    def __init__(self, cantormiddleware: CantorMiddleware, cantorcontroller: CantorController):
        self.cantormiddleware = cantormiddleware
        self.cantorcontroller = cantorcontroller
        self.blueprint = Blueprint('Cantor', __name__)
        print("⬆️ RouterCantor.constructor()")
        
    def createRoutes(self):
        # CREATE
        @self.blueprint.route('/cantores', methods=['POST'], endpoint='create_cantor')
        @token_required
        @self.cantormiddleware.validar_body_create  # ✅ CORRIGIDO
        def store():
            return self.cantorcontroller.store()
        
        # READ ALL
        @self.blueprint.route('/cantores', methods=['GET'], endpoint='list_cantores')
        @token_required
        def index():
            return self.cantorcontroller.index()
        
        # READ ONE
        @self.blueprint.route('/cantores/<int:idCantor>', methods=['GET'], endpoint='show_cantor')
        @token_required
        @self.cantormiddleware.validar_id_cantor  # ✅ CORRIGIDO
        def show(idCantor):
            return self.cantorcontroller.show(idCantor)
        
        # UPDATE
        @self.blueprint.route('/cantores/<int:idCantor>', methods=['PUT'], endpoint='update_cantor')
        @token_required
        @self.cantormiddleware.validar_id_cantor  # ✅ CORRIGIDO
        @self.cantormiddleware.validar_body_update  # ✅ CORRIGIDO
        def update(idCantor):
            return self.cantorcontroller.update(idCantor)
        
        # DELETE
        @self.blueprint.route('/cantores/<int:idCantor>', methods=['DELETE'], endpoint='delete_cantor')
        @token_required
        @self.cantormiddleware.validar_id_cantor  # ✅ CORRIGIDO
        def destroy(idCantor):
            return self.cantorcontroller.destroy(idCantor)
        
        return self.blueprint