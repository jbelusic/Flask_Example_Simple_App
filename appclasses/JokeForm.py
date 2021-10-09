# Klasa forme za unos
from . import ConnectionData
from . import Db_connection

class JokeForm:
    def __init__(self):
		# Inicijalizacija varijabli za konekciju
        self.db_variable = ConnectionData.ConnectionData()

		# Stvaramo konekciju
        self.db_conn = Db_connection.Db_connection( self.db_variable.getUser(),
                                                    self.db_variable.getPass(),
                                                    self.db_variable.getHost(),
                                                    self.db_variable.getPort(),
                                                    self.db_variable.getBase() )   

    def show(self):
        # Konekcija na bazu
        self.db_conn.connect()

        db_query = """SELECT c.id, c.name FROM "category" as c ORDER BY 1"""
        records = self.db_conn.get_data(db_query)

        print("Podaci za prikaz forme za unos su dohvaćeni\n")

        # Zatvaramo konekciju
        self.db_conn.disconnect()

        return records