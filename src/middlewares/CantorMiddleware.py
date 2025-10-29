from functools import wraps
from flask import request
from src.utils.ErrorResponse import ErrorResponse

class CantorMiddleware:
    
    def validateBody(self,f):
        @wraps
        def decorated_function(*args, **kwargs):
            print ("🔷 CantorMiddleware.validate_body()")

            body = request.get_json()
            
            requiredFields = ['nomeCantor', 'nacionalidade', 'idade', 'sexo', 'IdGravadora', 'IdFeatFamoso']
            missing = [field for field in requiredFields if field not in body or not body[field]] # lambda 
            
            if not body or missing:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": f"Os campos obrigatórios estão faltando: {', '.join(missing)}"}
                )
            return f(*args, **kwargs)
        return (decorated_function)
    
        
    def validateIdParam(self, f):
        # *args = argumentos posicionais (sem nome)
        # **kwargs = argumentos nomeados (com nome)
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 CantorMiddleware.validate_id_param()")
            if 'IdCantor' not in kwargs: #ps: é necessario que idUsuario tenha o mesmo nome que esta na rota
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O parâmetro 'id' é obrigatório!"}
                )
            return f(*args, **kwargs)
        return decorated_function
    
     