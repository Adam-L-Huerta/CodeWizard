import pymongo
from pymongo import MongoClient
import bcrypt


class RegisterModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.CodeWizard
        self.users = self.db.users

    def insert_user(self, data):
        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
        id = self.users.insert({"username": data.username, "name": data.name, "email": data.email, "password": hashed})
        print("uid is:", id)

        my_user = self.users.find_one({"username": data.username})

        if bcrypt.checkpw("12345".encode(), my_user["password"]):
            print("This matches.")

