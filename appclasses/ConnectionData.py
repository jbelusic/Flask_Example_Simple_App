# Globalne varijable koje se mogu dohvatiti iz config datoteke
class ConnectionData:
    def __init__(self):
        self.db_user = "crozuser"
        self.db_pass = ""
        self.db_host = "127.0.0.1"
        self.db_port = "5432"
        self.db_name = "postgres"

        print("Podaci za konekciju su inicijalizirani\n")

    def getUser(self):
        return self.db_user

    def getPass(self):
        return self.db_pass

    def getHost(self):
        return self.db_host

    def getPort(self):
        return self.db_port

    def getBase(self):
        return self.db_name