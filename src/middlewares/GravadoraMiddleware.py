from functools import wraps
from flask import request
from src.utils.ErrorResponse import ErrorResponse

class GravadoraMiddleware:
    def __init__(self):
        print("✅ GravadoraMiddleware initialized")

    def validar_body_create(self, f):
        """Valida body para criação de gravadora (POST)"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Verifica se é JSON
                if not request.is_json:
                    raise ErrorResponse(400, "Body inválido", "O corpo da requisição deve ser JSON")
                
                body = request.get_json()
                
                # Verifica se body não está vazio
                if not body:
                    raise ErrorResponse(400, "Body inválido", "O corpo da requisição está ausente ou incompleto")
                
                # Campos obrigatórios
                campos_obrigatorios = ['nomeGravadora', 'localizacao']
                for campo in campos_obrigatorios:
                    if campo not in body or not body[campo]:
                        raise ErrorResponse(400, "Campo obrigatório ausente", f"O campo '{campo}' é obrigatório")
                
                return f(*args, **kwargs)
            except ErrorResponse as e:
                raise e
            except Exception as e:
                raise ErrorResponse(500, "Erro interno no middleware de Gravadora", str(e))
        return decorated_function

    def validar_body_update(self, f):
        """Valida body para atualização de gravadora (PUT)"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Verifica se é JSON
                if not request.is_json:
                    raise ErrorResponse(400, "Body inválido", "O corpo da requisição deve ser JSON")
                
                body = request.get_json()
                
                # Verifica se body não está vazio
                if not body:
                    raise ErrorResponse(400, "Body inválido", "O corpo da requisição está ausente ou incompleto")
                
                # Para update, pelo menos um campo deve estar presente
                campos_permitidos = ['nomeGravadora', 'localizacao']
                if not any(campo in body for campo in campos_permitidos):
                    raise ErrorResponse(400, "Body inválido", "Pelo menos um campo deve ser informado para atualização")
                
                return f(*args, **kwargs)
            except ErrorResponse as e:
                raise e
            except Exception as e:
                raise ErrorResponse(500, "Erro interno no middleware de Gravadora", str(e))
        return decorated_function

    def validar_id_gravadora(self, f):
        """Valida se ID da gravadora foi informado na rota"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if 'idGravadora' not in kwargs:
                    raise ErrorResponse(400, "Requisição inválida", "O ID da gravadora não foi informado na rota")
                return f(*args, **kwargs)
            except ErrorResponse as e:
                raise e
            except Exception as e:
                raise ErrorResponse(500, "Erro interno no middleware de Gravadora", str(e))
        return decorated_function