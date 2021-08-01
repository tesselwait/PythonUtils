import sys
from PIL import Image
import random
import numpy as np
import re
import hashlib
from pathlib import Path

def removeSpecialCharacters(str):
    regex = "[^A-Za-z .?!,\"\-\*\']"
    return (re.sub(regex, "", str))

def removeNumericCharacters(str):
    regex = "[0-9]"
    return (re.sub(regex, "", str))

sourceText = Path("the_cosmic_looters.txt").read_text().replace('\n', ' ')
strippedText = removeNumericCharacters(removeSpecialCharacters(sourceText)).lower()
print(strippedText)

# Hide text in image via rgb adjustments to random pixels
arr = np.asarray(Image.open("thecosmiclooters.jpg"))
arr2 = arr.copy()
picture_width = len(arr)
picture_height = len(arr[0])
pixels = picture_width * picture_height
message = strippedText
pixelList = []
def num_to_pair(num, width):
    pair = [None] * 2
    pair[1] = int(num/width)
    pair[0] = num - (pair[1]*width)
    return pair
indexList = list(range(0, pixels-1))
for x in range(0, len(message)):
    pixelList.append(indexList.pop(random.randint(0, len(indexList)-1)))
pixelList.sort() # message characters assigned to pixels in order
for pixel in pixelList:
    pair = (num_to_pair(pixel, picture_width))
    charAscii = ord(message[pixelList.index(pixel)])
    if 96 < charAscii < 123:
        char_val = charAscii - 96
    elif message[pixelList.index(pixel)]==' ':
        char_val = 27
    elif message[pixelList.index(pixel)]=='.':
        char_val = 28
    elif message[pixelList.index(pixel)]==',':
        char_val = 29
    elif message[pixelList.index(pixel)]=='"':
        char_val = 30
    elif message[pixelList.index(pixel)]=='\'':
        char_val = 31
    elif message[pixelList.index(pixel)]=='!':
        char_val = 32
    elif message[pixelList.index(pixel)]=='?':
        char_val = 33
    elif message[pixelList.index(pixel)]=='-':
        char_val = 34
    elif message[pixelList.index(pixel)]=='*':
        char_val = 35
    r = 10 if (char_val) > 10 else (char_val)
    if char_val > 20:
        g = 10
    elif char_val > 10:
        g = char_val - 10
    else:
        g = 0
    b = 0 if (char_val) < 21 else (char_val - 20)
    if arr2[pair[0]][pair[1]][0] > 245:
        r = -r
    if arr2[pair[0]][pair[1]][1] > 245:
        g = -g
    if arr2[pair[0]][pair[1]][2] > 240:
        b = -b
    arr2[pair[0]][pair[1]][0] += r
    arr2[pair[0]][pair[1]][1] += g
    arr2[pair[0]][pair[1]][2] += b
augment = Image.fromarray(arr2)
augment.save("augmented_cosmic_looters.jpg")

def hash(img):
    return hashlib.md5(img.tobytes()).hexdigest()

def blacklight(orig, alt):
    if hash(orig) == hash(alt):
        print("Images are identical")
        return 0
    orig = orig.astype('int16')
    alt = alt.astype('int16')
    hidden_message = ""
    for m in range(0, len(orig[0])):
        for n in range(0, len(orig)):
            a = abs(alt[n][m][0] - orig[n][m][0])
            b = abs(alt[n][m][1] - orig[n][m][1])
            c = abs(alt[n][m][2] - orig[n][m][2])
            d = a + b + c
            if d != 0:
                print("Modification at: "+ str(m) + ", " + str(n))
                print("Old: "+str(orig[n][m][0] + orig[n][m][1] + orig[n][m][2])+", New: "+ str(alt[n][m][0] + alt[n][m][1] + alt[n][m][2]))
                letter = chr(d+96)
                if d == 27:
                    letter = ' '
                elif d == 28:
                    letter = '.'
                elif d == 29:
                    letter = ','
                elif d == 30:
                    letter = '\"'
                elif d == 31:
                    letter = '\''
                elif d == 32:
                    letter = '!'
                elif d == 33:
                    letter = '?'
                elif d == 34:
                    letter = '-'
                elif d == 35:
                    letter = '*'
                print("Difference: " + str(d) + " Letter: " + letter)
                print()
                hidden_message+=letter
    print("Hidden Message: " + hidden_message)
blacklight(arr, arr2)
