from src.models.Usuario import Usuario
from src.dao.UsuarioDAO import UsuarioDAO
from src.utils.ErrorResponse import ErrorResponse
import bcrypt

class UsuarioService:
    def __init__(self, daoUserDependency: UsuarioDAO):
        self.daoUserDependency = daoUserDependency 
        print("✅ UsuarioService initialized")
  
    def createUser(self, usuarioBodyRequest: dict) -> int:
       
        # Extrai dados do body request
        nome = usuarioBodyRequest.get("nome")
        email = usuarioBodyRequest.get("email")
        senha = usuarioBodyRequest.get("senha")
        
        # Validações
        if not nome or len(nome) < 3:
            raise ErrorResponse(400,
                                "Nome deve ter pelo menos 3 caracteres"
                                )
        
        if not email or '@' not in email:
            raise ErrorResponse(400,
                                "Email inválido"
                                )
        
        if not senha or len(senha) < 6:
            raise ErrorResponse(400,
                                "Senha deve ter pelo menos 6 caracteres"
                                )
        
        # Verifica se email já existe
        usuario_existente = self.daoUserDependency.findByEmail(email)
        if usuario_existente:  # Se existe, não pode cadastrar
            raise ErrorResponse(400,
                                "Email já está em uso",
                                {"email": email}
                                )
        
        # Hasheia a senha
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # explicando cada campo do hashpw:
        # senha.encode('utf-8') -> converte a senha para bytes
        # bcrypt.gensalt() -> gera um salt aleatório ( pode receber um parâmetro rounds para definir a complexidade)
        # .decode('utf-8') -> converte o hash de volta para string para guardar no banco
        
        # Cria objeto Usuario populado
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash
        )
        
        print("✅ UsuarioService.createUser()")
        return self.daoUserDependency.create(usuario)
    
    def updateUser(self, usuarioBodyRequest: dict, idUsuario: int) -> bool:
       
        
        # Busca usuário existente
        usuario_existente = self.daoUserDependency.findById(idUsuario)
        
        if not usuario_existente:
            raise ErrorResponse(404,
                                "Usuário não encontrado",
                                {"idUsuario": idUsuario}
                                )
        
        # Pega dados novos ou mantém antigos (atualização parcial)
        nome = usuarioBodyRequest.get("nome", usuario_existente['nome'])
        email = usuarioBodyRequest.get("email", usuario_existente['email'])
        
        # Validações
        if len(nome) < 3:
            raise ErrorResponse(400,
                                "Nome deve ter pelo menos 3 caracteres"
                                )
        
        if '@' not in email:
            raise ErrorResponse(400,
                                "Email inválido"
                                )
        
        # Verifica se email já existe em outro usuário
        if email != usuario_existente['email']:
            usuario_com_email = self.daoUserDependency.findByEmail(email)
            if usuario_com_email and usuario_com_email['idUsuario'] != idUsuario:
                raise ErrorResponse(400,
                                    "Email já está em uso por outro usuário"
                                    )
        
        # Trata senha (se enviada, hasheia; se não, mantém antiga)
        if 'senha' in usuarioBodyRequest:
            senha_nova = usuarioBodyRequest['senha']
            if len(senha_nova) < 6:
                raise ErrorResponse(400,
                                    "Senha deve ter pelo menos 6 caracteres"
                                    )
            senha_hash = bcrypt.hashpw(senha_nova.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            senha_hash = usuario_existente['senha_hash']
        
        # Cria objeto Usuario atualizado
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash,
            idUsuario=idUsuario
        )
        
        # Atualiza no banco
        sucesso = self.daoUserDependency.update(usuario)
        
        if not sucesso:
            raise ErrorResponse(500,
                                "Falha ao atualizar usuário"
                                )
        
        print("✅ UsuarioService.update()")
        return sucesso
    
    
    def deleteUser(self, idUsuario: int) -> bool:
        
        # Verifica se existe
        usuario = self.daoUserDependency.findById(idUsuario)
        if not usuario:
            raise ErrorResponse(404,
                                "Usuário não encontrado",
                                {"idUsuario": idUsuario}
                                )
                                
        
        sucesso = self.daoUserDependency.delete(idUsuario)
        
        print("✅ UsuarioService.delete()")
        return sucesso
    
    
    def findAll(self) -> list[dict]:
        
        usuarios = self.daoUserDependency.findAll()
        
        # Remove senha_hash dos resultados (segurança)
        for usuario in usuarios:
            usuario.pop('senha_hash', None) 
        
        print("✅ UsuarioService.findAll()")
        return usuarios
    
    
    def findById(self, idUsuario: int) -> dict | None:
        
        
        usuario = self.daoUserDependency.findById(idUsuario)
        
        if not usuario:
            raise ErrorResponse(404,
                                "Usuário não encontrado",
                                {"idUsuario": idUsuario}
                                )
        
        # Remove senha_hash (segurança)
        usuario.pop('senha_hash', None)
        
        print("✅ UsuarioService.findById()")
        return usuario # devolve dict completo sem senha_hash
    
    def authenticateUser(self, email: str, senha: str) -> dict:
        """Autentica usuário e retorna seus dados"""
        
        # Busca usuário por email
        usuario = self.daoUserDependency.findByEmail(email)
        
        if not usuario:
            raise ErrorResponse(401, "Email ou senha inválidos")
        
        # Verifica senha
        senha_valida = bcrypt.checkpw(
            senha.encode('utf-8'),
            usuario['senha_hash'].encode('utf-8')
        )
        
        if not senha_valida:
            raise ErrorResponse(401, "Email ou senha inválidos")
        
        # Remove senha_hash antes de retornar
        usuario.pop('senha_hash', None)
        
        print("✅ UsuarioService.authenticateUser()")
        return usuario