import sys
from PIL import Image
import random
import numpy as np
## Hide message in image by making slight rgb value adjustments
## to randomly selected pixels. (a-z) no spaces or punctuation
## Message length must be less than product of image dimensions
example_jpg = "Whiskey_Sour.jpg"
example_image = Image.open(example_jpg)
arr = np.asarray(example_image)
arr2 = arr.copy()
picture_width = len(arr)
picture_height = len(arr[0])
pixels = picture_width * picture_height
message = "awhiskeysourwithicecubesandalemonslice"
message_length = len(message)
list = []
def num_to_pair(num, width):
  pair = [None] * 2
  pair[1] = int(num/width)
  pair[0] = pixel - (pair[1]*width)
  return pair
for x in range(0, message_length):
    num_one = random.randint(0, pixels-1)
    list.append(num_one)
list.sort() # message characters assigned to pixels in order l->r t->b
for pixel in list:
    pair = (num_to_pair(pixel, picture_width))
    char_val = ord(message[list.index(pixel)])-96
    r = 10 if (char_val) > 10 else (char_val)
    if char_val > 20:
        g = 10
    elif char_val > 10:
        g = char_val - 10
    else:
        g = 0
    b = 0 if (char_val) < 21 else (char_val - 20)
    arr2[pair[0]][pair[1]][0] += r # message corruption
    arr2[pair[0]][pair[1]][1] += g # possible on pixel
    arr2[pair[0]][pair[1]][2] += b # rgb values > 245
augment = Image.fromarray(arr2)
augment.save("Augmented_Whiskey_Sour.jpg")
