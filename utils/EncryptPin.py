from cryptography.fernet import Fernet
from config import Settings

configs = Settings()

key = configs.ENCRYPTION_KEY

f = Fernet(key)

print(f, "f")

def encrypt_pin(pin):
    pin_bytes = str(pin).encode('utf-8')
    return f.encrypt(pin_bytes)

def decrypt_pin(pin):
    decrypted_bytes = f.decrypt(pin)
    return decrypted_bytes.decode('utf-8')








