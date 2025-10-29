"""
==================================================================
                    APLICAÇÃO FLASK - API REST
==================================================================
Sistema de gerenciamento de Cantores, Gravadoras e Feats
com autenticação JWT e banco de dados MySQL.
==================================================================
"""

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# ============================================
# IMPORTAÇÕES - CONFIG & DATABASE
# ============================================
from src.config.database import DatabaseConfig

# ============================================
# IMPORTAÇÕES - MODELS
# ============================================
from src.models.Usuario import Usuario
from src.models.Cantor import Cantor
from src.models.Gravadora import Gravadora
from src.models.FeatFamoso import FeatFamoso

# ============================================
# IMPORTAÇÕES - DAOs
# ============================================
from src.dao.UsuarioDAO import UsuarioDAO
from src.dao.CantorDAO import CantorDAO
from src.dao.GravadoraDAO import GravadoraDAO
from src.dao.FeatFamosoDAO import FeatFamosoDAO

# ============================================
# IMPORTAÇÕES - SERVICES
# ============================================
from src.services.UsuarioService import UsuarioService
from src.services.CantorService import CantorService
from src.services.GravadoraService import GravadoraService
from src.services.FeatFamosoService import FeatFamosoService

# ============================================
# IMPORTAÇÕES - CONTROLLERS
# ============================================
from src.controlles.UsuarioController import UsuarioController
from src.controlles.CantorController import CantorController
from src.controlles.GravadoraController import GravadoraController
from src.controlles.FeatFamosoController import FeatFamosoController

# ============================================
# IMPORTAÇÕES - MIDDLEWARES
# ============================================
from src.middlewares.ErrorMiddleware import ErrorMiddleware
from src.middlewares.UsuarioMiddleware import UserMiddleware
from src.middlewares.CantorMiddleware import CantorMiddleware
from src.middlewares.GravadoraMiddleware import GravadoraMiddleware
from src.middlewares.FeatFamosoMiddleware import FeatFamosoMiddleware

# ============================================
# IMPORTAÇÕES - ROUTERS
# ============================================
from src.routes.AuthRouter import AuthRouter
from src.routes.CantorRouter import CantorRouter
from src.routes.GravadoraRouter import GravadoraRouter
from src.routes.FeatFamosoRouter import FeatFamosoRouter


# ============================================
# CARREGA VARIÁVEIS DE AMBIENTE
# ============================================
load_dotenv()
print("✅ Variáveis de ambiente carregadas")


# ============================================
# INICIALIZAÇÃO DO FLASK
# ============================================
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # Mantém ordem dos campos no JSON
CORS(app)  # Habilita CORS para todas as rotas
print("✅ Aplicação Flask inicializada")


# ============================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================
database_config = DatabaseConfig(
    pool_name="api_pool",
    pool_size=10,
    pool_reset_session=True,
    host=os.getenv('DB_HOST', '127.0.0.1'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', 'Henry45*1'),
    database=os.getenv('DB_NAME', 'banco_cantores'),
    port=int(os.getenv('DB_PORT', 3306))
)
print("✅ Configuração de banco de dados criada")


# ============================================
# INJEÇÃO DE DEPENDÊNCIAS - USUARIO
# ============================================
# Camada DAO
usuario_dao = UsuarioDAO(database_config)

# Camada Service
usuario_service = UsuarioService(usuario_dao)

# Camada Controller
usuario_controller = UsuarioController(usuario_service)

# Middleware
usuario_middleware = UserMiddleware()

# Router
auth_router = AuthRouter(usuario_middleware, usuario_controller)

print("✅ Módulo de Usuário configurado")


# ============================================
# INJEÇÃO DE DEPENDÊNCIAS - CANTOR
# ============================================
# Camada DAO
cantor_dao = CantorDAO(database_config)

# Camada Service
cantor_service = CantorService(cantor_dao)

# Camada Controller
cantor_controller = CantorController(cantor_service)

# Middleware
cantor_middleware = CantorMiddleware()

# Router
cantor_router = CantorRouter(cantor_middleware, cantor_controller)

print("✅ Módulo de Cantor configurado")


# ============================================
# INJEÇÃO DE DEPENDÊNCIAS - GRAVADORA
# ============================================
# Camada DAO
gravadora_dao = GravadoraDAO(database_config)

# Camada Service
gravadora_service = GravadoraService(gravadora_dao)

# Camada Controller
gravadora_controller = GravadoraController(gravadora_service)

# Middleware
gravadora_middleware = GravadoraMiddleware()

# Router
gravadora_router = GravadoraRouter(gravadora_middleware, gravadora_controller)

print("✅ Módulo de Gravadora configurado")


# ============================================
# INJEÇÃO DE DEPENDÊNCIAS - FEATFAMOSO
# ============================================
# Camada DAO
feat_dao = FeatFamosoDAO(database_config)

# Camada Service
feat_service = FeatFamosoService(feat_dao)

# Camada Controller
feat_controller = FeatFamosoController(feat_service)

# Middleware
feat_middleware = FeatFamosoMiddleware()

# Router
feat_router = FeatFamosoRouter(feat_middleware, feat_controller)

print("✅ Módulo de FeatFamoso configurado")


# ============================================
# REGISTRO DE MIDDLEWARES GLOBAIS
# ============================================
ErrorMiddleware.register_error_handlers(app)
print("✅ Middleware de erros registrado")


# ============================================
# REGISTRO DE BLUEPRINTS (ROTAS)
# ============================================
# Rotas de Autenticação e Usuários
print ("PArou aquui!!!")
app.register_blueprint(
        auth_router.createRoutes(),
        url_prefix='/api/auth'
    )
    

    # Rotas de Cantores
app.register_blueprint(
        cantor_router.createRoutes(),
        url_prefix='/api'
    )
    

    # Rotas de Gravadoras
app.register_blueprint(
        gravadora_router.createRoutes(),
        url_prefix='/api'
    )
    

    # Rotas de Feats
app.register_blueprint(
        feat_router.createRoutes(),
        url_prefix='/api'
    )
    


# ============================================
# ROTA RAIZ (TESTE)
# ============================================
@app.route('/')
def home():
    """Rota raiz para testar se a API está funcionando"""
    return jsonify({
        "success": True,
        "message": "🎵 API de Cantores está online!",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "cantores": "/api/cantores",
            "gravadoras": "/api/gravadoras",
            "feats": "/api/feats"
        }
    }), 200


# ============================================
# ROTA DE HEALTH CHECK
# ============================================
@app.route('/health')
def health_check():
    """Verifica se a API e o banco estão funcionando"""
    try:
        # Testa conexão com o banco
        with database_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        
        return jsonify({
            "success": True,
            "status": "healthy",
            "database": "connected",
            "message": "API e banco de dados funcionando normalmente"
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500


# ============================================
# ROTA DE DOCUMENTAÇÃO (OPCIONAL)
# ============================================
@app.route('/api/docs')
def api_docs():
    """Documentação básica da API"""
    return jsonify({
        "title": "API de Gestão de Cantores",
        "version": "1.0.0",
        "description": "API REST para gerenciar cantores, gravadoras e feats famosos",
        "authentication": "JWT Bearer Token",
        "endpoints": {
            "auth": {
                "POST /api/auth/register": "Cadastrar novo usuário",
                "GET /api/auth/users": "Listar usuários (protegido)",
                "GET /api/auth/users/<id>": "Buscar usuário (protegido)",
                "PUT /api/auth/users/<id>": "Atualizar usuário (protegido)",
                "DELETE /api/auth/users/<id>": "Deletar usuário (protegido)"
            },
            "cantores": {
                "POST /api/cantores": "Criar cantor (protegido)",
                "GET /api/cantores": "Listar cantores (protegido)",
                "GET /api/cantores/<id>": "Buscar cantor (protegido)",
                "PUT /api/cantores/<id>": "Atualizar cantor (protegido)",
                "DELETE /api/cantores/<id>": "Deletar cantor (protegido)"
            },
            "gravadoras": {
                "POST /api/gravadoras": "Criar gravadora (protegido)",
                "GET /api/gravadoras": "Listar gravadoras (protegido)",
                "GET /api/gravadoras/<id>": "Buscar gravadora (protegido)",
                "PUT /api/gravadoras/<id>": "Atualizar gravadora (protegido)",
                "DELETE /api/gravadoras/<id>": "Deletar gravadora (protegido)"
            },
            "feats": {
                "POST /api/feats": "Criar feat (protegido)",
                "GET /api/feats": "Listar feats (protegido)",
                "GET /api/feats/<id>": "Buscar feat (protegido)",
                "PUT /api/feats/<id>": "Atualizar feat (protegido)",
                "DELETE /api/feats/<id>": "Deletar feat (protegido)"
            }
        },
        "example_request": {
            "register": {
                "method": "POST",
                "url": "/api/auth/register",
                "body": {
                    "nome": "Drake",
                    "email": "drake@email.com",
                    "senha": "senha123"
                }
            },
            "protected_route": {
                "method": "GET",
                "url": "/api/cantores",
                "headers": {
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                }
            }
        }
    }), 200


# ============================================
# INICIALIZAÇÃO DO SERVIDOR
# ============================================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 INICIANDO SERVIDOR FLASK")
    print("="*60)
    print(f"📍 URL: http://127.0.0.1:5000")
    print(f"📍 Documentação: http://127.0.0.1:5000/api/docs")
    print(f"📍 Health Check: http://127.0.0.1:5000/health")
    print("="*60 + "\n")
    
    # Modo de desenvolvimento (debug=True)
    # Em produção, use debug=False
    app.run(
        host='0.0.0.0',  # Aceita conexões de qualquer IP
        port=5000,       # Porta padrão
        debug=True       # Modo debug (auto-reload e mensagens detalhadas)
    )