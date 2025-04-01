from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
from app.config import ENCRYPTION_KEY

def encrypt_message(plaintext: str) -> str:
    iv = get_random_bytes(16)
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode()

def decrypt_message(encrypted_payload: str) -> str:
    raw = base64.b64decode(encrypted_payload)
    iv, ciphertext = raw[:16], raw[16:]
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()