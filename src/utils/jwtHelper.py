import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request
from src.utils.ErrorResponse import ErrorResponse
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
TOKEN_EXPIRATION_HOURS = 24


# ✅ Função solta (não classe)
def gerar_token(user_id: int, email: str) -> str:
    """Gera um token JWT para o usuário"""
    payload = {
        'user_id': user_id,  # ✅ Só ID
        'email': email,      # ✅ Só email 
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def validar_token(token: str) -> dict:
    """Valida e decodifica um token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ErrorResponse(401, "Token expirado")
    except jwt.InvalidTokenError:
        raise ErrorResponse(401, "Token inválido")


def token_required(f):
    """Decorator para proteger rotas que precisam de autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
            except IndexError:
                raise ErrorResponse(401, "Formato de token inválido")
        
        if not token:
            raise ErrorResponse(401, "Token não fornecido")
        
        # Valida o token
        payload = validar_token(token)
        
        # Adiciona dados do usuário no request
        request.user_id = payload['user_id']
        request.email = payload['email']
        
        return f(*args, **kwargs)
    
    return decorated