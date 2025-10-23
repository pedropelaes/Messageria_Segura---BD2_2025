from User import User
from Database import Database


class Mensageria:
    def __init__(self):
        self.db = Database()
        self.user = None


    def showMessages(self):
        print("Suas mensagens:")
        messages = self.db.getUserMessages(self.user.nome)
        if(len(messages) == 0):
            print("Você não tem nenhuma mensagem.\n")
        else:
            print(messages)

    def sendMessage(self, destinatario, title, body):
        result = self.db.createMessage(self.user.nome, destinatario, title, body,)
        if(result == -1): print("O titulo pode ter no máximo 20 caracteres.")


    def start(self):
        print("###Bem vindo a mensageria segura!###" \
        "Faça login para visualizar e enviar suas mensagens!\n")
        nome = ""
        sel = 0
        while sel!=2:
            sel = int(input("Digite:\n1 - Login\n2-Sair\n"))

            if(sel == 1):
                nome = input("Digite seu nome:\n")
                while(not nome):
                    nome = input("Digite seu nome novamente:\n")
                if(nome[0] != '@'): nome = '@' + nome
                result = self.db.login(nome)
                if(result != None):
                    self.user = User(nome)
                    print(f"#Seja bem vindo, {self.user.nome}")
                    sel2 = 0
                    while(sel2 != 3):
                        print("Digite:\n 1 - Suas mensagens\n 2 - Enviar mensagem\n3 - voltar")
                        sel2 = int(input())
                        if(sel2!= 1 and sel2!=2 and sel2!=3): sel2 = int(input("Digite uma opção válida:\n"))
                        if(sel2 == 1):
                            self.showMessages()
                        if(sel2 == 2):
                            title = input("Digite o titulo da mensagem(máximo 20 caracteres):\n")
                            body = input("Digite o corpo da mensagem:\n")
                            destinatario = input("Digite para quem você quer enviar essa mensagem:\n")
                            if(self.db.login(destinatario) == None):
                                destinatario = input("Usuario não encontrado, tente novamente:\n")
                            if(destinatario[0] != '@'): destinatario = '@' + destinatario
                            self.sendMessage(destinatario, title, body)
                        if(sel2 == 3):
                            self.user = None
                            

                else:
                    print("Usuario não encontrado\n")


m = Mensageria()
m.start()

            