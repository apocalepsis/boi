import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]
key = "4=Z3H4Z$H4Q7esMD]6Y,(^BU"
hash_key = hashlib.sha256(key.encode('utf-8')).digest()

def encrypt(raw):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new( hash_key, AES.MODE_CBC, iv )
    return base64.b64encode(iv+cipher.encrypt(raw))

def decrypt(enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(hash_key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt(enc[16:]))
