from src.models.Usuario import Usuario
from src.config.database import DatabaseConfig

class UsuarioDAO:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        print("✅ UsuarioDAO initialized")
             
    def create(self, usuario: Usuario) -> int:
        conn = None
        cursor = None
        try:
            query = "INSERT INTO Usuario (nome, email, senha_hash) VALUES (%s, %s, %s)"
            values = (usuario.getNome(), usuario.getEmail(), usuario.getSenha())
            
            conn = self.db_config.get_connection() # conecta com o banco
            cursor = conn.cursor()          # instancia o cursor
            cursor.execute(query, values)   # executa o codigo sql
            conn.commit()                   # "confirma" o codigo sql 
            insert_id = cursor.lastrowid    # pega o ultimo id criado (ja que é auto increment)
            
            if not insert_id:
                raise Exception("Falha ao inserir usuário")
            
            print("✅ UsuarioDAO.create()")
            return insert_id
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                     
    def delete(self, idUsuario: int) -> bool:
        conn = None
        cursor = None
        try:
            query = "DELETE FROM Usuario WHERE idUsuario = %s"
            values = (idUsuario,)
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            
            print("✅ UsuarioDAO.delete()")
            return affected_rows > 0
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                 
    def update(self, usuario: Usuario) -> bool:
        conn = None
        cursor = None
        try:
            query = "UPDATE Usuario SET nome = %s, email = %s, senha_hash = %s WHERE idUsuario = %s"
            values = (usuario.getNome(), usuario.getEmail(), usuario.getSenha(), usuario.getIdUsuario())
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            
            print("✅ UsuarioDAO.update()")
            return affected_rows > 0
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                      
    def findAll(self) -> list[dict]:
        conn = None
        cursor = None
        try:
            query = "SELECT * FROM Usuario"
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            
            print(f"✅ UsuarioDAO.findAll() -> {len(results)} registros")
            return results
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                 
    def findById(self, idUsuario: int) -> dict | None:
        conn = None
        cursor = None
        try:
            query = "SELECT * FROM Usuario WHERE idUsuario = %s"
            values = (idUsuario,)
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, values)
            result = cursor.fetchone()
            
            print("✅ UsuarioDAO.findById()")
            return result
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
         
    def findByField(self, field: str, value) -> list[dict]:
        conn = None
        cursor = None
        try:
            allowed_fields = ['idUsuario', 'nome', 'email', 'senha_hash']
            if field not in allowed_fields:
                raise ValueError(f"Campo inválido para busca: {field}")
            
            query = f"SELECT * FROM Usuario WHERE {field} = %s"
            values = (value,)
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, values)
            results = cursor.fetchall()
            
            print("✅ UsuarioDAO.findByField()")
            return results
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
         
    def findByEmail(self, email: str) -> dict | None:
        resultados = self.findByField('email', email)
        return resultados[0] if resultados else None
    

        