from functools import wraps
from flask import request
from src.utils.ErrorResponse import ErrorResponse


class UserMiddleware:

    def validateBody(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 UserMiddleware.validate_body()")
            body = request.get_json() # recolhe o body enviado pelo usuario

            if not body or 'email' not in body or 'senha' not in body or 'nome' not in body:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'nome', 'email' e 'senha' são obrigatórios! Verifique se inseriu todos os campos!"}
                )

            return f(*args, **kwargs)
        return decorated_function
    
    def validateIdParam(self, f):
        # *args = argumentos posicionais (sem nome)
        # **kwargs = argumentos nomeados (com nome)
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 UserMiddleware.validate_id_param()")
            if 'IdUsuario' not in kwargs: #ps: é necessario que idUsuario tenha o mesmo nome que esta na rota
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O parâmetro 'id' é obrigatório!"}
                )
            return f(*args, **kwargs)
        return decorated_function
    
    
             
            
