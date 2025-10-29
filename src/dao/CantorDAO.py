from src.models.Cantor import Cantor
from src.config.database import DatabaseConfig 

class CantorDAO:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        print("✅ CantorDAO initialized")
        
    def create(self, cantor: Cantor) -> int:
        conn = None
        cursor = None
        try:
            query = "INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, Gravadora_idGravadora, FeatFamoso_idFeat) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (cantor.getNomeCantor(),
                      cantor.getNacionalidade(),
                      cantor.getIdade(),
                      cantor.getSexo(),
                      cantor.getGravadora_id(),
                      cantor.getFeat_id())
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            insert_id = cursor.lastrowid
            
            if not insert_id:
                raise Exception("Falha ao inserir cantor")
            
            print("✅ CantorDAO.create()")
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
                
    def delete(self, idCantor: int) -> bool:
        conn = None
        cursor = None
        try:
            query = "DELETE FROM Cantor WHERE idCantor = %s"
            values = (idCantor,)
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            
            print("✅ CantorDAO.delete()")
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
            
    def update(self, cantor: Cantor) -> bool:
        conn = None
        cursor = None
        try:
            query = "UPDATE Cantor SET nomeCantor = %s, nacionalidade = %s, idade = %s, sexo = %s, Gravadora_idGravadora = %s, FeatFamoso_idFeat = %s WHERE idCantor = %s"
            values = (cantor.getNomeCantor(),
                      cantor.getNacionalidade(),
                      cantor.getIdade(),
                      cantor.getSexo(),
                      cantor.getGravadora_id(),
                      cantor.getFeat_id(),
                      cantor.getIdCantor())
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            
            print("✅ CantorDAO.update()")
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
            query = "SELECT * FROM Cantor"
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            print(f"✅ CantorDAO.findAll() -> {len(resultados)} registros encontrados")
            return resultados
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def findById(self, idCantor: int) -> dict | None:
        resultados = self.findByField("idCantor", idCantor)
        print("✅ CantorDAO.findById()")
        return resultados[0] if resultados else None 
    
    def findByField(self, field: str, value) -> list[dict]: 
        conn = None
        cursor = None
        try:
            allowed_fields = ["idCantor", "nomeCantor", "nacionalidade", "idade", "sexo", "Gravadora_idGravadora", "FeatFamoso_idFeat"]
            if field not in allowed_fields:
                raise ValueError(f"Campo inválido para busca: {field}")
            
            query = f"SELECT * FROM Cantor WHERE {field} = %s"
            params = (value,)
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            
            print("✅ CantorDAO.findByField()")
            return resultados
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()