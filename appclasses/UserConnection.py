# Klasa koja rukuje korisničkim spajanjima i dozvoljenim vremenom logiranja
from . import AuthData

class UserConnection:
    def __init__(self):
        self.auth_data = AuthData.AuthData()

    def checkIfexists(self, username):
        if self.isBlank(username):
            return False

        if self.auth_data.getUser(username):
            return True

    def isBlank (self, myString):
        return not (myString and myString.strip())