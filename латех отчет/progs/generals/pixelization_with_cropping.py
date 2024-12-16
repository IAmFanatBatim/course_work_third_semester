from PIL import Image
import numpy as np
 
#Get a name of image in "images" folder and read an image
filename = input()
img = Image.open("images/" + filename)
 
#Get a size of "pixels" on result image
cell_size = int(input())

#Get a size of cropped image and cropped image itself
cropped_width = img.width - img.width % cell_size
cropped_height = img.height - img.height % cell_size
img = img.crop((img.width % cell_size // 2, img.height % cell_size // 2, img.width % cell_size // 2 + cropped_width, img.height % cell_size // 2 + cropped_height))

#Convert image object into array and open it for writing
arrayImg = np.array(img)
arrayImg.setflags(write=1)

#Iterate all possible cells
for row in range(0, arrayImg.shape[0], cell_size):
    for col in range(0, arrayImg.shape[1], cell_size):
        #Get color-array for average of all colors in cell
        cur_pixel = arrayImg[row:row+cell_size, col:col+cell_size].sum(axis=(0,1))
        cur_pixel = cur_pixel // cell_size**2
        #Paint all pixels of cell in average color
        arrayImg[row:row+cell_size, col:col+cell_size] = cur_pixel

img2 = Image.fromarray(arrayImg)
img2.save("images/pixel_" + filename)
