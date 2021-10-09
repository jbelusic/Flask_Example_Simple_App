class AuthData:
    def __init__(self):
        self.users = {
            "pperic": "pero",
            "iivic": "ivan"
        }
    
    def getUser(self, user):
        return self.users.get(user)