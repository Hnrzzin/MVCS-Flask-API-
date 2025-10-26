from src.models.FeatFamoso import FeatFamoso
from src.config.database import DatabaseConfig 

class FeatFamosoDAO:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        
    def create(self, feat: FeatFamoso) -> int:
        query = "INSERT INTO FeatFamoso (nomeFeat, cantorFeat, streams) VALUES (%s, %s, %s)"
        values = (feat.getNomeFeat(),
                  feat.getCantorFeat(),
                  feat.getStreams())
        # with serve para abrir e fechar a conexão automaticamente
        with self.db_config.get_connection() as conn: 
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                insert_id = cursor.lastrowid
                
                if not insert_id:
                    raise Exception("Falha ao inserir feat famoso")
                
                print("✅ FeatFamosoDAO.create()")
                return insert_id
                
    def delete(self, feat: FeatFamoso) -> bool:
        query = "DELETE FROM FeatFamoso WHERE idFeat = %s"
        values = (feat.getIdFeat(),)
        
        with self.db_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                affected_rows = cursor.rowcount
                print("✅ FeatFamosoDAO.delete()")
                return affected_rows > 0
            
    def update(self, feat: FeatFamoso) -> bool:
        query = "UPDATE FeatFamoso SET nomeFeat = %s, cantorFeat = %s, streams = %s WHERE idFeat = %s"
        values = (feat.getNomeFeat(),
                  feat.getCantorFeat(),
                  feat.getStreams(),
                  feat.getIdFeat())
        
        with self.db_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                affected_rows = cursor.rowcount
                print("✅ FeatFamosoDAO.update()")
                return affected_rows > 0
            
    def findAll(self) -> list[dict]:
        query = "SELECT * FROM FeatFamoso;"

        with self.db_config.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                resultados = cursor.fetchall()

        print(f"✅ FeatFamosoDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados

    def findById(self, idFeat: int) -> dict | None:
        resultados = self.findByField("idFeat", idFeat)
        print("✅ FeatFamosoDAO.findById()")
        return resultados[0] if resultados else None 
    
    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idFeat", "nomeFeat", "cantorFeat", "streams"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        query = f"SELECT * FROM FeatFamoso WHERE {field} = %s;"
        params = (value,)

        with self.db_config.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()

        print("✅ FeatFamosoDAO.findByField()")
        return resultados