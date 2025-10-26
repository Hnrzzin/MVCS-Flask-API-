from src.models.Gravadora import Gravadora
from src.config.database import DatabaseConfig 

class GravadoraDAO:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
    
    # Create   
    def create(self, gravadora: Gravadora) -> int:
        query = "INSERT INTO Gravadora (nomeGravadora, localizacao) VALUES (%s, %s)"
        values = (gravadora.getNomeGravadora(),
                  gravadora.getLocalizacao())
        
        with self.db_config.get_connection() as conn: 
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                insert_id = cursor.lastrowid
                
                if not insert_id:
                    raise Exception("Falha ao inserir gravadora")
                
                print("✅ GravadoraDAO.create()")
                return insert_id
            
    # Deleta pelo id            
    def delete(self, gravadora: Gravadora) -> bool:
        query = "DELETE FROM Gravadora WHERE idGravadora = %s"
        values = (gravadora.getIdGravadora(),)
        
        with self.db_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                affected_rows = cursor.rowcount
                print("✅ GravadoraDAO.delete()")
                return affected_rows > 0
            
    # update em relação ao id      
    def update(self, gravadora: Gravadora) -> bool:
        query = "UPDATE Gravadora SET nomeGravadora = %s, localizacao = %s WHERE idGravadora = %s"
        values = (gravadora.getNomeGravadora(),
                  gravadora.getLocalizacao(),
                  gravadora.getIdGravadora())
        
        with self.db_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                affected_rows = cursor.rowcount
                print("✅ GravadoraDAO.update()")
                return affected_rows > 0
     
    # busca todos os registros       
    def findAll(self) -> list[dict]:
        query = "SELECT * FROM Gravadora;"

        with self.db_config.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                resultados = cursor.fetchall()

        print(f"✅ GravadoraDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados
    
    # depende do findByField
    # busca o registro pelo id
    def findById(self, idGravadora: int) -> dict | None:
        resultados = self.findByField("idGravadora", idGravadora)
        print("✅ GravadoraDAO.findById()")
        return resultados[0] if resultados else None 
    
    # Encontra registros por um campo específico
    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idGravadora", "nomeGravadora", "localizacao"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        query = f"SELECT * FROM Gravadora WHERE {field} = %s;"
        params = (value,)

        with self.db_config.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()

        print("✅ GravadoraDAO.findByField()")
        return resultados