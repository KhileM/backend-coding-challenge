from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from app.config import ENCRYPTION_KEY

def broken_decrypt(encrypted_payload):
    raw = base64.b64decode(encrypted_payload)
    iv = raw[:8]  # ❌ Incorrect: should be 16 bytes
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
    return cipher.decrypt(raw[8:]).decode('utf-8', errors='ignore')  # ❌ Missing unpad

def fixed_decrypt(encrypted_payload):
    raw = base64.b64decode(encrypted_payload)
    iv = raw[:16]
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(raw[16:]), AES.block_size).decode()