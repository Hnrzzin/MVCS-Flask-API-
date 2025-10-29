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
from src.controlles.UsuarioController import UsuarioController  # ✅ CORRIGIDO
from src.controlles.CantorController import CantorController      # ✅ CORRIGIDO
from src.controlles.GravadoraController import GravadoraController  # ✅ CORRIGIDO
from src.controlles.FeatFamosoController import FeatFamosoController  # ✅ CORRIGIDO

# ============================================
# IMPORTAÇÕES - MIDDLEWARES
# ============================================
from src.middlewares.ErrorMiddleware import ErrorMiddleware
from src.middlewares.UsuarioMiddleware import UsuarioMiddleware  # ✅ CORRIGIDO
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
    pool_size=25,
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
usuario_dao = UsuarioDAO(database_config)
usuario_service = UsuarioService(usuario_dao)
usuario_controller = UsuarioController(usuario_service)
usuario_middleware = UsuarioMiddleware()  # ✅ CORRIGIDO
auth_router = AuthRouter(usuario_middleware, usuario_controller)
print("✅ Módulo de Usuário configurado")


# ============================================
# INJEÇÃO DE DEPENDÊNCIAS - CANTOR
# ============================================
cantor_dao = CantorDAO(database_config)
cantor_service = CantorService(cantor_dao)
cantor_controller = CantorController(cantor_service)
cantor_middleware = CantorMiddleware()
cantor_router = CantorRouter(cantor_middleware, cantor_controller)
print("✅ Módulo de Cantor configurado")


# ============================================
# INJEÇÃO DE DEPENDÊNCIAS - GRAVADORA
# ============================================
gravadora_dao = GravadoraDAO(database_config)
gravadora_service = GravadoraService(gravadora_dao)
gravadora_controller = GravadoraController(gravadora_service)
gravadora_middleware = GravadoraMiddleware()
gravadora_router = GravadoraRouter(gravadora_middleware, gravadora_controller)
print("✅ Módulo de Gravadora configurado")


# ============================================
# INJEÇÃO DE DEPENDÊNCIAS - FEATFAMOSO
# ============================================
feat_dao = FeatFamosoDAO(database_config)
feat_service = FeatFamosoService(feat_dao)
feat_controller = FeatFamosoController(feat_service)
feat_middleware = FeatFamosoMiddleware()
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
print("🔧 Registrando blueprints...")

# Rotas de Autenticação e Usuários
app.register_blueprint(
    auth_router.createRoutes(),
    url_prefix='/api/auth'
)
print("  ✅ Rotas de Auth registradas")

# Rotas de Cantores
app.register_blueprint(
    cantor_router.createRoutes(),
    url_prefix='/api'
)
print("  ✅ Rotas de Cantor registradas")

# Rotas de Gravadoras
app.register_blueprint(
    gravadora_router.createRoutes(),
    url_prefix='/api'
)
print("  ✅ Rotas de Gravadora registradas")

# Rotas de Feats
app.register_blueprint(
    feat_router.createRoutes(),
    url_prefix='/api'
)
print("  ✅ Rotas de Feat registradas")


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
    conn = None
    cursor = None
    try:
        # Pega conexão do pool
        conn = database_config.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
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
    
    finally:
        # Fecha cursor e devolve conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            conn.close()


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
                "POST /api/auth/cadastro": "Cadastrar novo usuário",
                "POST /api/auth/login": "Fazer login",
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
        }
    }), 200


# ============================================
# INICIALIZAÇÃO DO SERVIDOR
# ============================================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 INICIANDO SERVIDOR FLASK")
    print("="*60)
    print(f"🌐 URL: http://127.0.0.1:5000")
    print(f"📚 Documentação: http://127.0.0.1:5000/api/docs")
    print(f"💊 Health Check: http://127.0.0.1:5000/health")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )