import pymongo, bcrypt
from pymongo import MongoClient


class LoginModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.CodeWizard
        self.users = self.db.users

    def check_login(self, data):
        user = self.users.find_one({"username": data.username})
        pw = data.password.encode()

        if user:
            if bcrypt.checkpw(pw, user["password"]):
                return user
            else:
                return False
        else:
            return False
