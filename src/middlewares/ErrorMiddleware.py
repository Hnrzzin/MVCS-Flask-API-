from flask import jsonify
from src.utils.ErrorResponse import ErrorResponse

class ErrorMiddleware:
    """Middleware global para capturar e formatar erros"""
    
    @staticmethod
    def register_error_handlers(app):
        """Registra os handlers de erro na aplicação Flask"""
        
        @app.errorhandler(ErrorResponse)
        def handle_error_response(error: ErrorResponse):
            """Handler para ErrorResponse customizado"""
            print(f"🔴 ErrorMiddleware: Capturou erro {error}")
            
            return jsonify({ # usa somente os getters
                "success": False,
                "httpCode": error.getHttpCode(),  
                "message": error.getMessage(),     
                "error": error.getError()          
            }), error.getHttpCode()
        
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({
                "success": False,
                "httpCode": 404,
                "message": "Rota não encontrada",
                "error": str(error)
            }), 404
        
        @app.errorhandler(500)
        def internal_error(error):
            return jsonify({
                "success": False,
                "httpCode": 500,
                "message": "Erro interno do servidor",
                "error": str(error)
            }), 500
            
        @app.errorhandler(400)
        def request_error(error):
            return jsonify({
                "success": False,
                "httpCode": 400,
                "message": "Erro ao validar os dados",
                "error": str(error)
            }), 400
        
        @app.errorhandler(Exception)
        def handle_generic_exception(error):
            print(f"🔴 ErrorMiddleware: Exceção genérica: {str(error)}")
            return jsonify({
                "success": False,
                "httpCode": 500,
                "message": "Erro interno do servidor",
                "error": str(error)
            }), 500
        
        print("✅ ErrorMiddleware registrado com sucesso")