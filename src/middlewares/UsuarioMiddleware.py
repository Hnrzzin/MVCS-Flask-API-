from functools import wraps
from flask import request
from src.utils.ErrorResponse import ErrorResponse

class UsuarioMiddleware:
    def __init__(self):
        print("✅ UsuarioMiddleware initialized")

    def validar_body_create(self, f):
        """Valida body para criação de usuário (POST)"""
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
                
                # Campos obrigatórios para criar
                campos_obrigatorios = ['nome', 'email', 'senha']
                for campo in campos_obrigatorios:
                    if campo not in body or not body[campo]:
                        raise ErrorResponse(400, "Campo obrigatório ausente", f"O campo '{campo}' é obrigatório")
                
                return f(*args, **kwargs)
            except ErrorResponse as e:
                raise e
            except Exception as e:
                raise ErrorResponse(500, "Erro interno no middleware de Usuario", str(e))
        return decorated_function

    def validar_body_update(self, f):
        """Valida body para atualização de usuário (PUT)"""
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
                campos_permitidos = ['nome', 'email', 'senha']
                if not any(campo in body for campo in campos_permitidos):
                    raise ErrorResponse(400, "Body inválido", "Pelo menos um campo deve ser informado para atualização")
                
                return f(*args, **kwargs)
            except ErrorResponse as e:
                raise e
            except Exception as e:
                raise ErrorResponse(500, "Erro interno no middleware de Usuario", str(e))
        return decorated_function

    def validar_body_login(self, f):
        """Valida body para login"""
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
                
                # Campos obrigatórios para login
                campos_obrigatorios = ['email', 'senha']
                for campo in campos_obrigatorios:
                    if campo not in body or not body[campo]:
                        raise ErrorResponse(400, "Campo obrigatório ausente", f"O campo '{campo}' é obrigatório")
                
                return f(*args, **kwargs)
            except ErrorResponse as e:
                raise e
            except Exception as e:
                raise ErrorResponse(500, "Erro interno no middleware de Usuario", str(e))
        return decorated_function

    def validar_id_usuario(self, f):
        """Valida se ID do usuário foi informado na rota"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if 'idUsuario' not in kwargs:
                    raise ErrorResponse(400, "Requisição inválida", "O ID do usuário não foi informado na rota")
                return f(*args, **kwargs)
            except ErrorResponse as e:
                raise e
            except Exception as e:
                raise ErrorResponse(500, "Erro interno no middleware de Usuario", str(e))
        return decorated_function