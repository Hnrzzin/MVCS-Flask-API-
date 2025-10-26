import jwt                                # Biblioteca para criar/validar tokens JWT
from datetime import datetime, timedelta  # Manipular datas (expiração)
from functools import wraps               # Preservar metadados do decorator
from flask import request                 # Acessar dados da requisição HTTP
from src.utils.ErrorResponse import ErrorResponse  # Exceção customizada
from dotenv import load_dotenv
import os

load_dotenv()

# Acessa as variáveis
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
TOKEN_EXPIRATION_HOURS = 24

def gerar_token(user_id: int, email: str) -> str:
    
    # Gera um token JWT para o usuário
    payload = {
        'user_id': user_id, 
        'email': email,
        'exp': datetime.now() + timedelta(hours=TOKEN_EXPIRATION_HOURS), 
        'iat': datetime.now() 
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # payload + chave + algoritmo
    return token

def validar_token(token: str) -> dict:
    # Valida e decodifica um token JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    # Erro personalizado para token expirado ( do proprio framework jwt)
    except jwt.ExpiredSignatureError: 
        raise ErrorResponse(401, "Token expirado")
    except jwt.InvalidTokenError:
        raise ErrorResponse(401, "Token inválido")

# Decorator para proteger rotas
def token_required(f): # função resposnavel por proteger rotas
    @wraps(f)                       
    def decorated(*args, **kwargs): # decorated serve para envolver a função original
        token = None
        
        # Pega token do header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # "Bearer TOKEN"
            except IndexError:
                raise ErrorResponse(401, "Formato de token inválido")
        
        if not token:
            raise ErrorResponse(401, "Token não fornecido")
        
        # Valida o token
        payload = validar_token(token)
        
        # Adiciona dados do usuário no request
        request.user_id = payload['user_id']
        request.email = payload['email']
        
        return f(*args, **kwargs) # Chama a função original
    
    return decorated 