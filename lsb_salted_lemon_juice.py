from PIL import Image
import numpy as np
import random
import hashlib
from pathlib import Path
import secrets
import base64
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#  Program encrypts text from a .txt file with a password and embeds the ciphertext onto a .png file using steganography.
#  Ciphertext is then extracted from the new .png file by comparison with the original and decrypted.

backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)

ciphertext_dict = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4,
    'E': 5, 'F': 6, 'G': 7, 'H': 8,
    'I': 9, 'J': 10, 'K': 11, 'L': 12,
    'M': 13, 'N': 14, 'O': 15, 'P': 16,
    'Q': 17, 'R': 18, 'S': 19, 'T': 20,
    'U': 21, 'V': 22, 'W': 23, 'X': 24,
    'Y': 25, 'Z': 26, 'a': 27, 'b': 28,
    'c': 29, 'd': 30, 'e': 31, 'f': 32,
    'g': 33, 'h': 34, 'i': 35, 'j': 36,
    'k': 37, 'l': 38, 'm': 39, 'n': 40,
    'o': 41, 'p': 42, 'q': 43, 'r': 44,
    's': 45, 't': 46, 'u': 47, 'v': 48,
    'w': 49, 'x': 50, 'y': 51, 'z': 52,
    '0': 53, '1': 54, '2': 55, '3': 56,
    '4': 57, '5': 58, '6': 59, '7': 60,
    '8': 61, '9': 62, '-': 63, '_': 64,
    '=': 65, "'": 66
    }

ciphertext_list = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '_', '=', "'"]

sourceText = Path("declaration_of_independence.txt").read_text().replace('\n', ' ')
message = sourceText
print("Message: "+message)
print()
password = 'asdf1234ASDF4567'
token_text = password_encrypt(message.encode(), password)
print("Ciphertext:")
print(type(token_text))
print(token_text)
print()

arr = np.asarray(Image.open("Whiskey_Sour.jpg"))
arr2 = arr.copy()
picture_width = len(arr)
picture_height = len(arr[0])
pixels = picture_width * picture_height
message_string = token_text.decode('ascii')
#eq_count = message_string.count('=')
#message_string = message_string[:-eq_count]
print("Cipher_String:")
print(type(message_string))
print(message_string)
print()

pixelList = []
def num_to_pair(num, width):
    pair = [None] * 2
    pair[1] = int(num/width)
    pair[0] = num - (pair[1]*width)
    return pair
indexList = list(range(0, pixels-1))
for x in range(0, len(message_string)):
    pixelList.append(indexList.pop(random.randint(0, len(indexList)-1)))
pixelList.sort()
for pixel in pixelList:
    pair = (num_to_pair(pixel, picture_width))
    char_val = ciphertext_dict[message_string[pixelList.index(pixel)]]
    char_binary = format(char_val, "b").zfill(7)
    r = int(char_binary[:3], 2)
    g = int(char_binary[3:5], 2)
    b = int(char_binary[5:], 2)

    if arr2[pair[0]][pair[1]][0] > 250:
        r = -r
    if arr2[pair[0]][pair[1]][1] > 250:
        g = -g
    if arr2[pair[0]][pair[1]][2] > 250:
        b = -b
    arr2[pair[0]][pair[1]][0] += r
    arr2[pair[0]][pair[1]][1] += g
    arr2[pair[0]][pair[1]][2] += b


augment = Image.fromarray(arr2)
augment.save("Salted_Whiskey_Sour.png")

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
                e = int(str(format(a, "b").zfill(3)) + str(format(b, "b").zfill(2)) + str(format(c, "b").zfill(2)), 2)
                #print("Modification at: "+ str(m) + ", " + str(n))
                #print("Old: "+str(orig[n][m][0] + orig[n][m][1] + orig[n][m][2])+", New: "+ str(alt[n][m][0] + alt[n][m][1] + alt[n][m][2]))
                letter = ciphertext_list[e]
                #print("Difference: " + str(d) + " Letter: " + letter)
                #print()
                hidden_ciphertext+=letter
    #print("Hidden Message: " + hidden_ciphertext)
    return hidden_ciphertext
hidden_cipher = blacklight(np.asarray(Image.open("Whiskey_Sour.jpg")), np.asarray(Image.open("Salted_Whiskey_Sour.png")))
hidden_cipher_bytes = hidden_cipher.encode('ascii')
#print("Extracted cipher bytes:")
#print(type(hidden_cipher_bytes))
#print(hidden_cipher_bytes)
#print()
print("Decrypted Message:")
decrypted_cipher = password_decrypt(hidden_cipher_bytes, password).decode()
print(decrypted_cipher)
