from src.models.Cantor import Cantor
from src.config.database import DatabaseConfig 

class CantorDAO:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        
    def create(self, cantor: Cantor) -> int:
        query = "INSERT INTO Cantor (nomeCantor, nacionalidade, idade, sexo, idGravadora, idFeat) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (cantor.getNomeCantor(),
                  cantor.getNacionalidade(),
                  cantor.getIdade(),
                  cantor.getSexo(),
                  cantor.getGravadora_id(),
                  cantor.getFeat_id(), 
                  )
        # faz a conexão com o banco de dados
        with self.__database.get_connection() as conn: 
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                insert_id = cursor.lastrowid # lastrowid pega o id do último registro inserido
                
                if not insert_id:
                    raise Exception("Falha ao inserir cargo")
                
                print("✅ CargoDAO.create()")
                return insert_id
                
    def delete (self,cantor: Cantor) -> bool:
        query = "DELETE FROM Cantor WHERE idCantor = %s"
        values = (cantor.idCantor(),)
        
        with self.db_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                affected_rows = cursor.rowcount
                print("✅ CantorDAO.delete()")
                return affected_rows > 0 # só vai retornar True se tiver deletado algum registro
            
    # ver como funciona esse update (em relação ao id)        
    def update (self, cantor: Cantor) -> bool:
        query = "UPDATE Cantor SET nomeCantor = %s, nacionalidade = %s, idade = %s, sexo = %s, idGravadora = %s, idFeat = %s WHERE idCantor = %s"
        values = (cantor.getNomeCantor(),
                  cantor.getNacionalidade(),
                  cantor.getIdade(),
                  cantor.getSexo(),
                  cantor.getGravadora_id(),
                  cantor.getFeat_id(),
                  cantor.getIdCantor())
        
        with self.db_config.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                affected_rows = cursor.rowcount
                print("✅ CantorDAO.update()")
                # se affected_rows > 0 retorna True, ou seja, se algum registro foi atualizado
                return affected_rows > 0 
            
    # faz a busca de todos os cantores               
    def findAll(self) -> list[dict]: # retorna uma lista de dicionários 
        query = "SELECT * FROM Cantor;"

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor: # dictionary=True para retornar os resultados como dicionários
                cursor.execute(query)
                resultados = cursor.fetchall()

        print(f"✅ CantorDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados

    # retorna um dicionário ou None
    def findById(self, idCantor: int) -> dict | None:
        resultados = self.findByField("idCantor", idCantor)
        print("✅ CantorDAO.findById()")
        return resultados[0] if resultados else None 
    
    # retorna uma lista de dicionários
    # busca por uma coluna de uma tabela
    # field (nome dda coluna), value (valor a ser buscado)
    # por que usar? Evita criar 7 funções diferentes (uma para cada campo)!
    # allowed_fields é uma lista de campos permitidos para busca (limita os campos que podem ser usados)
    def findByField(self, field: str, value) -> list[dict]: 
        allowed_fields = ["idCantor", "nomeCantor", "nacionalidade", "idade", "sexo", "idGravadora", "idFeat"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        query = f"SELECT * FROM Cantor WHERE {field} = %s;"
        params = (value,)

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()

        print("✅ CantorDAO.findByField()")
        return resultados