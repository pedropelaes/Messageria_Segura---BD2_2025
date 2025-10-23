from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv 
import os



class Database:
    def __init__(self):
        load_dotenv()
        MONGO_URI = os.getenv("MONGO_URI")
        self.db = MongoClient(MONGO_URI)["Mensageria"]
    
    def login(self, name):
        users = self.db["users"]
        return users.find_one({"nome" : name})
    
    def getUserMessages(self, name):
        messages = self.db["messages"].find({"destinatario": name})
        return list(messages)
    
    def createMessage(self, remetente, destinatario, title, body):
        if(len(title) > 20):
            return -1
        message = {
            "titulo" : title,
            "corpo" : body,
            "remetente": remetente,
            "destinatario" : destinatario,
        }
        try:
            self.db["messages"].insert_one(message)
            print("Mensagem enviada\n")
        except PyMongoError as e:
            print("Erro ao enviar mensagem: ", e)




