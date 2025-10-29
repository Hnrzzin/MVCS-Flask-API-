from flask import Blueprint
from src.utils.jwtHelper import token_required
from src.middlewares.CantorMiddleware import CantorMiddleware
from src.controlles.CantorController import CantorController

class CantorRouter:
    
    def __init__(self, cantormiddleware: CantorMiddleware, cantorcontroller: CantorController):
        self.cantormiddleware = cantormiddleware
        self.cantorcontroller = cantorcontroller
        self.blueprint = Blueprint('Cantor', __name__)
        print("⬆️ RouterCantor.contructor()")
        
    def createRoutes(self):
        # CREATE
        @self.blueprint.route('/cantores', methods=['POST'], endpoint='create_cantor')
        @token_required
        @self.cantormiddleware.validateBody
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
        @self.cantormiddleware.validateIdParam
        def show(idCantor):
            return self.cantorcontroller.show(idCantor)  # ✅ Passa o ID
        
        # UPDATE
        @self.blueprint.route('/cantores/<int:idCantor>', methods=['PUT'], endpoint='update_cantor')
        @token_required
        @self.cantormiddleware.validateBody
        @self.cantormiddleware.validateIdParam
        def update(idCantor):
            return self.cantorcontroller.update(idCantor)  # ✅ Passa o ID
        
        # DELETE
        @self.blueprint.route('/cantores/<int:idCantor>', methods=['DELETE'], endpoint='delete_cantor')
        @token_required
        @self.cantormiddleware.validateIdParam
        def destroy(idCantor):
            return self.cantorcontroller.destroy(idCantor)  # ✅ Passa o ID
        
        return self.blueprint