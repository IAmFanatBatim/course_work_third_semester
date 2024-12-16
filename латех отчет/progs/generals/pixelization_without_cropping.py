from PIL import Image
import numpy as np
 
#Get a name of image in "images" folder and read an image
filename = input()
img = Image.open("images/" + filename)
 
#Convert image object into array and open it for writing
arrayImg = np.array(img)
arrayImg.setflags(write=1)

#Get a size of "pixels" on result image
cell_size = int(input())

#Iterate all possible cells
for row in range(0, arrayImg.shape[0], cell_size):
    for col in range(0, arrayImg.shape[1], cell_size):
        #Get color-array for average of all colors in cell
        cur_pixel = arrayImg[row:row+cell_size, col:col+cell_size].sum(axis=(0,1))
        cur_pixel = cur_pixel // cell_size**2
        #Paint all pixels of cell in average color
        arrayImg[row:row+cell_size, col:col+cell_size] = cur_pixel

#Convert array into image object and save it in same folder
img2 = Image.fromarray(arrayImg)
img2.save("images/pixel_" + filename)
