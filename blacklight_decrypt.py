from PIL import Image
import numpy as np
import hashlib
from pathlib import Path
import secrets
import base64
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)

ciphertext_list = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '_', '=', "'"]

def hash(img):
    return hashlib.md5(img.tobytes()).hexdigest()

def blacklight(orig, alt):
    if hash(orig) == hash(alt):
        print("Images are identical")
        return 0
    orig = orig.astype('int16')
    alt = alt.astype('int16')
    hidden_ciphertext = ""
    for m in range(0, len(orig[0])):
        for n in range(0, len(orig)):
            a = abs(alt[n][m][0] - orig[n][m][0])
            b = abs(alt[n][m][1] - orig[n][m][1])
            c = abs(alt[n][m][2] - orig[n][m][2])
            d = a + b + c
            if d != 0:
            #    print("Modification at: "+ str(m) + ", " + str(n))
            #    print("Old: "+str(orig[n][m][0] + orig[n][m][1] + orig[n][m][2])+", New: "+ str(alt[n][m][0] + alt[n][m][1] + alt[n][m][2]))
                letter = ciphertext_list[d]
                #print("Difference: " + str(d) + " Letter: " + letter)
            #    print()
                hidden_ciphertext+=letter
    #print("Hidden Message: " + hidden_ciphertext)
    return hidden_ciphertext
hidden_cipher = blacklight(np.asarray(Image.open("Whiskey_Sour.jpg")), np.asarray(Image.open("Salted_Whiskey_Sour.png")))
print("Extracted Image Cipher String")
print(type(hidden_cipher))
print(hidden_cipher)
hidden_cipher_bytes = hidden_cipher.encode('ascii')
print()
print("Decrypted Message:")
decrypted_cipher = password_decrypt(hidden_cipher_bytes, "asdf1234ASDF1234").decode()
print(decrypted_cipher)
