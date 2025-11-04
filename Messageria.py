from User import User
from Database import Database


class Mensageria:
    def __init__(self):
        self.db = Database()
        self.user = None


    def getRemetentes(self):
        messages = self.db.getUserMessages(self.user.nome)
        if(len(messages) == 0):
            print("\n\n##Você não tem nenhuma mensagem.\n")
            return -1
        else:
            remetentes = {item["remetente"].replace("@", "") for item in messages}
            remetentes = list(remetentes)
            print(f"##Você tem mensagens de: {', '.join(remetentes)}" )
            return remetentes



    def sendMessage(self, destinatario, title, body, key):
        self.db.createMessage(self.user.nome, destinatario, title, body, key)


    def start(self):
        print("\n\n###Bem vindo a mensageria segura!###\n" \
        "##Faça login para visualizar e enviar suas mensagens!\n")
        nome = ""
        sel = 0
        while sel!=2:
            sel = int(input("#Digite:\n 1 - Login\n 2 - Sair\n"))

            if(sel == 1):
                nome = input("#Digite seu nome:\n")
                while(not nome):
                    nome = input("#Digite seu nome novamente:\n")
                if(nome[0] != '@'): nome = '@' + nome
                result = self.db.login(nome)
                if(result != None):
                    self.user = User(nome)
                    print(f"\n\n#Seja bem vindo, {self.user.nome}")
                    sel2 = 0
                    while(sel2 != 3):
                        print("\n#Digite:\n| 1 - Suas mensagens\n| 2 - Enviar mensagem\n| 3 - voltar")
                        sel2 = int(input())
                        if(sel2!= 1 and sel2!=2 and sel2!=3): sel2 = int(input("Digite uma opção válida:\n"))
                        if(sel2 == 1):
                            r = self.getRemetentes()
                            if(r != -1):
                                user = input("#Digite o nome do usuário que deseja visualizar as mensagens: ")
                                while(not user):
                                    user = input("#Digite um usuario válido: ")
                                while(user not in r):
                                    user = input("#Usuario não encontrado, digite novamente: ")
                                if(user[0] != '@'): user = '@' + user
                                key = input("#Digite a chave que você combinou com esse usuário:\n").encode()
                                m = self.db.getUserMessagesFrom(self.user.nome, user, key)
                                if not m:
                                    print("#Nenhuma mensagem disponível (talvez a chave esteja errada).")
                                else:
                                    for msg in m:
                                        print(f"##\n\nDe {msg['remetente']}\n Data:{msg['enviadoEm'].strftime("%d/%m/%Y %H:%M:%S")}\n Título: {msg['titulo']}\n Corpo: {msg['corpo']}")

                        if(sel2 == 2):
                            key = input("#Digite a chave de criptografia que você combinou com seu destinatário:\n").encode()
                            title = input("#Digite o titulo da mensagem(máximo 30 caracteres):\n")
                            while(len(title) > 30):
                                title = input("#Digite o titulo da mensagem(máximo 30 caracteres):\n")
                            body = input("#Digite o corpo da mensagem:\n")
                            user_valido = False
                            destinatario = ""
                            while not user_valido:
                                destinatario = input("#Digite para quem você quer enviar essa mensagem:\n")

                                if not destinatario:
                                    print("O nome do destinatário não pode ser vazio.")
                                    continue 
                                if not destinatario.startswith('@'):
                                    destinatario = '@' + destinatario
                                if self.db.login(destinatario) != None:
                                    user_valido = True 
                                else:
                                    print("#Usuario não encontrado, tente novamente:")
                            
                            self.sendMessage(destinatario, title, body, key)
                        if(sel2 == 3):
                            self.user = None
                            

                else:
                    print("#Usuario não encontrado\n")


m = Mensageria()
m.start()

            