from src.models.Gravadora import Gravadora
from src.config.database import DatabaseConfig 

class GravadoraDAO:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        print("✅ GravadoraDAO initialized")
        
    def create(self, gravadora: Gravadora) -> int:
        conn = None
        cursor = None
        try:
            query = "INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES (%s, %s)"
            values = (gravadora.getNomeGravadora(),
                      gravadora.getLocalizacao())
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            insert_id = cursor.lastrowid
            
            if not insert_id:
                raise Exception("Falha ao inserir gravadora")
            
            print("✅ GravadoraDAO.create()")
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
    
    def delete(self, idGravadora: int) -> bool:
        conn = None
        cursor = None
        try:
            query = "DELETE FROM Gravadora WHERE idGravadora = %s"
            values = (idGravadora,)
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            
            print("✅ GravadoraDAO.delete()")
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
    
    def update(self, gravadora: Gravadora) -> bool:
        conn = None
        cursor = None
        try:
            query = "UPDATE Gravadora SET nomeGravadora = %s, localizacao = %s WHERE idGravadora = %s"
            values = (gravadora.getNomeGravadora(),
                      gravadora.getLocalizacao(),
                      gravadora.getIdGravadora())
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            
            print("✅ GravadoraDAO.update()")
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
            query = "SELECT * FROM Gravadora"
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            print(f"✅ GravadoraDAO.findAll() -> {len(resultados)} registros encontrados")
            return resultados
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def findById(self, idGravadora: int) -> dict | None:
        resultados = self.findByField("idGravadora", idGravadora)
        print("✅ GravadoraDAO.findById()")
        return resultados[0] if resultados else None 
    
    def findByField(self, field: str, value) -> list[dict]:
        conn = None
        cursor = None
        try:
            allowed_fields = ["idGravadora", "nomeGravadora", "localizacao"]
            if field not in allowed_fields:
                raise ValueError(f"Campo inválido para busca: {field}")
            
            query = f"SELECT * FROM Gravadora WHERE {field} = %s"
            params = (value,)
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            
            print("✅ GravadoraDAO.findByField()")
            return resultados
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
