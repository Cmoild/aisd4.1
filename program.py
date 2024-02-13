from PIL import Image
import numpy as np

image = Image.open("istockphoto-1337005456-612x612.jpg")
#image.show()
img = np.asarray(image)
print(len(img[0]))