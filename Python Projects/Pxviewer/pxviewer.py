from PIL import Image
import numpy as np
import re
import ast

# Read the pixel values from the file
with open('output.txt', 'r') as file:
    content = file.read()

# Convert the string representation of lists into actual lists
pixels = ast.literal_eval(content)
    
# Convert the pixels into an array using numpy
array = np.array(pixels, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save('flag.png')

random_array = np.random.randint(low=0, high=255,size=(250,250),dtype=np.uint8)
random_im = Image.fromarray(random_array)
random_im.show()