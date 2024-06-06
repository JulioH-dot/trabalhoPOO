from src.models.professor_model import Professor

class ProfessorRepository:
    def __init__(self, database):
        self.database = database

    def create(self, professor):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                sql = "INSERT INTO Professor (Nome, Email, Senha) VALUES (%s, %s, %s) RETURNING ID"
                cursor.execute(sql, (professor.nome, professor.email, professor.senha))
                conn.commit()
                return cursor.fetchone()[0]

    def get_all(self):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Professor")
                return [Professor(*row) for row in cursor.fetchall()]
    
    def get_by_id(self, professor_id):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM Professor WHERE ID = %s"
                cursor.execute(sql, (professor_id,))
                professor = cursor.fetchone()
                if professor:
                    return Professor(*professor)
                else:
                    return None

    def update(self, professor):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                sql = "UPDATE Professor SET Nome = %s, Email = %s, Senha = %s WHERE ID = %s"
                cursor.execute(sql, (professor.nome, professor.email, professor.senha, professor.id))
                conn.commit()

    def delete(self, professor_id):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM Professor WHERE ID = %s"
                cursor.execute(sql, (professor_id,))
                conn.commit()
    
    def loginProfessor(self, email, senha): 
        # Verifica se as credenciais estão corretas
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM Professor WHERE Email = %s AND Senha = %s"
                cursor.execute(sql, (email, senha))
                professor = cursor.fetchone()
                return professor
            
    def get_by_email(self, email):
        with self.database.connect() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM Professor WHERE Email = %s"
                cursor.execute(sql, (email,))
                result = cursor.fetchone()
                if result:
                    professor = Professor(*result)
                    return professor
                else:
                    return None
