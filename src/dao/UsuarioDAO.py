from src.models.Usuario import Usuario
from src.config.database import DatabaseConfig

class UsuarioDAO:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        
    def create(self, usuario: Usuario) -> int:
        query = "INSERT INTO Usuario (nome, email, senha_hash) VALUES (%s, %s, %s)"
        values = (usuario.getNome(),
                  usuario.getEmail(),
                  usuario.getSenha())
        
        with self.db_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                insert_id = cursor.lastrowid
                
                if not insert_id:
                    raise Exception("Falha ao inserir usuário")
                
                print("✅ UsuarioDAO.create()")
                return insert_id
                
    def delete(self, idUsuario: int) -> bool:
        
        query = "DELETE FROM Usuario WHERE idUsuario = %s"
        values = (idUsuario,)
        
        with self.db_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                affected_rows = cursor.rowcount
                print("✅ UsuarioDAO.delete()")
                return affected_rows > 0
            
    def update(self, usuario: Usuario) -> bool:
        query = "UPDATE Usuario SET nome = %s, email = %s, senha_hash = %s WHERE idUsuario = %s"
        values = (usuario.getNome(),
                  usuario.getEmail(),
                  usuario.getSenha(),
                  usuario.getIdUsuario())  
        
        with self.db_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                affected_rows = cursor.rowcount
                print("✅ UsuarioDAO.update()")
                return affected_rows > 0
            
    
    def findAll(self) -> list[dict]:
        query = "SELECT * FROM Usuario"
        
        with self.db_config.get_connection() as conn:
            
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                   
                print(f"✅ UsuarioDAO.findAll() -> {len(results)} registros")
                return results
            
    def findById(self, idUsuario: int) -> dict | None:
        query = "SELECT * FROM Usuario WHERE idUsuario = %s"
        values = (idUsuario,)
        
        with self.db_config.get_connection() as conn:
            
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()
                
                print("✅ UsuarioDAO.findById()")
                return result
    
    def findByField(self, field: str, value) -> list[dict]:
        
        allowed_fields = ['idUsuario', 'nome', 'email', 'senha_hash'] # Campos permitidos para busca (presentes no banco)
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")
        
        query = f"SELECT * FROM Usuario WHERE {field} = %s"
        values = (value,)
        
        with self.db_config.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, values)
                results = cursor.fetchall()
                
                print("✅ UsuarioDAO.findByField()")
                return results
    
    # Buscar por email (útil para login)
    def findByEmail(self, email: str) -> dict | None:
        resultados = self.findByField('email', email)
        return resultados[0] if resultados else None