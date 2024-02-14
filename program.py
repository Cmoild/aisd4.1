from PIL import Image
import numpy as np

img = np.asarray(Image.open("istockphoto-1337005456-612x612.jpg")).copy()

for i in range(len(img)):
    for j in range(len(img[0])):
        if img[i][j] > 100:
            img[i][j] = 255
        else:
            img[i][j] = 0

new_img = Image.fromarray(img)
new_img.show()