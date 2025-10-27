from functools import wraps
from flask import request
from src.utils.ErrorResponse import ErrorResponse

class FeatFamosoMiddleware:
    
    def validateBody(self,f):
        @wraps
        def decorated_function(*args, **kwargs):
            print ("🔷 FeatFamosoMiddleware.validate_body()")

            body = request.get_json()
            
            requiredFields = ['nomeFeat', 'cantorFeat', 'streams']
            missing = [field for field in requiredFields if field not in body or not body[field]] # lambda 
            
            if not body or missing:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": f"Os campos obrigatórios estão faltando: {', '.join(missing)}"}
                )
            return f(*args, **kwargs)
        return (decorated_function)