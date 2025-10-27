from flask import jsonify
from src.utils.ErrorResponse import ErrorResponse

class ErrorMiddleware:
    
    
    @staticmethod # não precisa instanciar a classe quando for usar (corta caminho)
    def register_error_handlers(app):
       
        @app.errorhandler(ErrorResponse) # captura qualquer erro
        def handle_error_response(error: ErrorResponse):
            
            print(f"🔴 ErrorMiddleware: Capturou erro {error.httpCode}")
            
            return jsonify({
                "success": False,
                "message": error.args[0],      # Mensagem principal do erro
                "error": error.error           # Detalhes adicionais (dict ou None)
            }), error.httpCode
        
        
        @app.errorhandler(Exception) # captura erro de servidor
        def handle_generic_error(error: Exception):
           
            print(f"🔴 ErrorMiddleware: Erro não tratado: {str(error)}")
            
            return jsonify({
                "success": False,
                "message": "Erro interno do servidor",
                "error": str(error)
            }), 500
        
        
        @app.errorhandler(404)
        def handle_not_found(error): # captura erro de rota não encontrada
           
            return jsonify({
                "success": False,
                "message": "Rota não encontrada",
                "error": "A URL requisitada não existe nesta API"
            }), 404
        
        
        @app.errorhandler(405)
        def handle_method_not_allowed(error): # verifica se a requisição está correta
            
            return jsonify({
                "success": False,
                "message": "Método HTTP não permitido",
                "error": "Verifique se está usando GET, POST, PUT ou DELETE correto"
            }), 405
        
        
        print("✅ ErrorMiddleware registrado com sucesso")