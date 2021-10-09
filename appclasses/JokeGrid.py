# Klasa pregleda podataka
from . import ConnectionData
from . import Db_connection

class JokeGrid:
    def __init__(self):
        # Inicijalizacija varijabli za konekciju
        self.db_variable = ConnectionData.ConnectionData()

    def show(self):
		# Stvaramo konekciju
        db_conn = Db_connection.Db_connection(self.db_variable.getUser(),
								self.db_variable.getPass(),
								self.db_variable.getHost(),
								self.db_variable.getPort(),
								self.db_variable.getBase())

        # Konekcija na bazu
        db_conn.connect()

        db_query = """SELECT ROW_NUMBER () OVER (ORDER BY coalesce(j.likes,0) - coalesce(j.dislikes,0) desc) AS "#",
                             c.name AS "Kategorija",
                             j.content AS "Vic",
                             j.likes AS "Likes",
                             j.dislikes AS "Dislikes",
                             coalesce(j.likes,0) - coalesce(j.dislikes,0) AS "Razlika",
			                 j.id AS "joke_id"
                        FROM "joke" as j
                        LEFT JOIN "category" AS c ON (c.id = j.category_id)
                    ORDER BY 1"""

        records = db_conn.get_data(db_query)

        print("Podaci za prikaz su dohvaćeni\n")

        # Odspajamo se sa baze
        db_conn.disconnect()

        return records