import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Crypto:
    def __init__(self, chave):
        self.key = chave

    def generateKey(self, senha: str) -> bytes:
        salt = self.key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        return base64.urlsafe_b64encode(kdf.derive(senha))
    
    def encrypt(self, mensagem: str, senha: str) -> bytes:
        chave = self.generateKey(senha)
        f = Fernet(chave)
        return f.encrypt(mensagem.encode())

    def decrypt(self, mensagem_criptografada: bytes, senha: str) -> str:
        chave = self.generateKey(senha)
        f = Fernet(chave)
        return f.decrypt(mensagem_criptografada).decode()
    
    def safe_decrypt(self, mensagem_criptografada, key):
        try:
            return self.decrypt(mensagem_criptografada, key)
        except :
            # A chave está errada ou os dados foram corrompidos
            return None

