from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv 
import os

from Crypto import Crypto



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
    

    
    def getUserMessagesFrom(self, name, user, key):
        messages = self.db["messages"].find({"destinatario": name, "remetente" : user})
        crypto = Crypto(key)
        m_descriptografadas = []
        for m in messages:
            msg = m

            titulo = crypto.safe_decrypt(msg["titulo"], key)
            corpo = crypto.safe_decrypt(msg["corpo"], key)

            if(titulo is None or corpo is None):
                print("A chave está incorreta.")

            msg["titulo"] = titulo
            msg["corpo"] = corpo
            m_descriptografadas.append(msg)
        return list(m_descriptografadas)
        
        
    def createMessage(self, remetente, destinatario, title, body, key):  
        crypto = Crypto(key)
        message = {
            "titulo" : crypto.encrypt(title, key).decode(),
            "corpo" : crypto.encrypt(body, key).decode(),
            "remetente": remetente,
            "destinatario" : destinatario,
        }
        try:
            self.db["messages"].insert_one(message)
            print("Mensagem enviada\n")
        except PyMongoError as e:
            print("Erro ao enviar mensagem: ", e)

    def teste(self, key):
        crypto = Crypto(key)
        teste = crypto.encrypt("teste", key)
        print("Encrypt:", teste)
        print("Decrypt:", crypto.decrypt(teste, key))



