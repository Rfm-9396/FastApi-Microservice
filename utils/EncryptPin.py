from cryptography.fernet import Fernet
from config import Settings

configs = Settings()

key = configs.ENCRYPTION_KEY

f = Fernet(key)

print(f, "f")

def encrypt_pin(pin):
    print(f.encrypt(pin), "encrypted pin")
    return f.encrypt(pin)

def decrypt_pin(pin):
    return f.decrypt(pin)





