import sys
from PIL import Image
import random
import numpy as np
## Hide message in image by making slight rgb value adjustments
## to randomly selected pixels. (a-z) no spaces or punctuation
## Message length must be less than product of image dimensions
arr = np.asarray(Image.open("Whiskey_Sour.jpg"))
arr2 = arr.copy()
picture_width = len(arr)
picture_height = len(arr[0])
pixels = picture_width * picture_height
message = "awhiskeysourwithicecubesandalemonslice"
list = []
def num_to_pair(num, width):
  pair = [None] * 2
  pair[1] = int(num/width)
  pair[0] = num - (pair[1]*width)
  return pair
for x in range(0, len(message)):
  list.append(random.randint(0, pixels-1))
list.sort() # message characters assigned to pixels in order
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
  arr2[pair[0]][pair[1]][2] += b # values > 245
augment = Image.fromarray(arr2)
augment.save("Augmented_Whiskey_Sour.png")
def blacklight(orig, alt):
  hidden_message = ""
  for m in range(0, len(orig[0])):
    for n in range(0, len(orig)):
      a = orig[n][m][0] + orig[n][m][1] + orig[n][m][2]
      b = alt[n][m][0] + alt[n][m][1] + alt[n][m][2]
      if a != b:
        print("Modification at: "+ str(m) + ", " + str(n))
        print("Old: "+str(a)+", New: "+str(b))
        print("Difference: " + str(abs(b-a)) + " Letter: " + chr(abs(b-a)+96))
        print()
        hidden_message+=chr(abs(b-a)+96)
  print("Hidden Message: " + hidden_message)
blacklight(arr, arr2)
