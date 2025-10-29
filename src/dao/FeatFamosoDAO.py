from src.models.FeatFamoso import FeatFamoso
from src.config.database import DatabaseConfig 

class FeatFamosoDAO:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        print("✅ FeatFamosoDAO initialized")
        
    def create(self, feat: FeatFamoso) -> int:
        conn = None
        cursor = None
        try:
            query = "INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES (%s, %s, %s)"
            values = (feat.getNomeFeat(),
                      feat.getCantorFeat(),
                      feat.getStreams())
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            insert_id = cursor.lastrowid
            
            if not insert_id:
                raise Exception("Falha ao inserir feat famoso")
            
            print("✅ FeatFamosoDAO.create()")
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
    
    def delete(self, idFeat: int) -> bool:
        conn = None
        cursor = None
        try:
            query = "DELETE FROM FeatFamoso WHERE idFeat = %s"
            values = (idFeat,)
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            
            print("✅ FeatFamosoDAO.delete()")
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
    
    def update(self, feat: FeatFamoso) -> bool:
        conn = None
        cursor = None
        try:
            query = "UPDATE FeatFamoso SET nomeFeat = %s, cantorFeat = %s, streams = %s WHERE idFeat = %s"
            values = (feat.getNomeFeat(),
                      feat.getCantorFeat(),
                      feat.getStreams(),
                      feat.getIdFeat())
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            
            print("✅ FeatFamosoDAO.update()")
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
            query = "SELECT * FROM FeatFamoso"
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            print(f"✅ FeatFamosoDAO.findAll() -> {len(resultados)} registros encontrados")
            return resultados
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def findById(self, idFeat: int) -> dict | None:
        resultados = self.findByField("idFeat", idFeat)
        print("✅ FeatFamosoDAO.findById()")
        return resultados[0] if resultados else None 
    
    def findByField(self, field: str, value) -> list[dict]:
        conn = None
        cursor = None
        try:
            allowed_fields = ["idFeat", "nomeFeat", "cantorFeat", "streams"]
            if field not in allowed_fields:
                raise ValueError(f"Campo inválido para busca: {field}")
            
            query = f"SELECT * FROM FeatFamoso WHERE {field} = %s"
            params = (value,)
            
            conn = self.db_config.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            
            print("✅ FeatFamosoDAO.findByField()")
            return resultados
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
