import psycopg2

# Konekcija na bazu i diskonekcija
class Db_connection:
    def __init__(self, db_user, db_pass, db_host, db_port, database):
        self.usr           = db_user
        self.pwd           = db_pass
        self.host          = db_host
        self.port          = db_port
        self.db            = database
        self.connection    = False
        self.rows_inserted = 0

    def connect(self):
        try:
            self.connection = psycopg2.connect( user     = self.usr,
                                                password = self.pwd,
                                                host     = self.host,
                                                port     = self.port,
                                                database = self.db )
            print("PostgreSQL connected\n")
            return True

        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print("Error, alredy connected to PostgreSQL", error)
            else:
                print ("Error while connecting to PostgreSQL", error)

            return False

    def get_data(self, db_query):
        cursor = self.connection.cursor()
        cursor.execute(db_query)
        records = cursor.fetchall()
        cursor.close()

        return records #POSTGRES cursor returns List of tuples

    def insert_data(self, db_query):
        try:
			# Podaci za unos
            cursor = self.connection.cursor()
            cursor.execute(db_query)
            self.connection.commit()
            self.rows_inserted = cursor.rowcount
            cursor.close()
            
            print("Slog je unesen\n")
            return True
        except:
            print("Slog nije unesen\n")
            return False

    def disconnect(self):
        if(self.connection):
            self.connection.close()

        print("PostgreSQL connection closed\n")
        return True