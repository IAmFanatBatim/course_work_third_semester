from PIL import Image
import numpy as np
 
#Get a name of image in "images" folder and read an image
filename = input()
img = Image.open("images/" + filename)
 
#Get a size of "pixels" on result image
cell_size = int(input())
grid_size = max(cell_size//10, 1)

#Get a size of cropped image and cropped image itself
cells_in_width = img.width // cell_size
cells_in_height = img.height // cell_size

cropped_width = img.width - img.width % cell_size
cropped_height = img.height - img.height % cell_size

img = img.crop((img.width % cell_size // 2, img.height % cell_size // 2, img.width % cell_size // 2 + cropped_width, img.height % cell_size // 2 + cropped_height))

# convert image object into array
arrayImg = np.array(img)
arrayImg.setflags(write=1)

griddedImage = np.full((cropped_height + (cells_in_height-1)*grid_size, cropped_width + (cells_in_width-1)*grid_size, 3), 128)

for i in range(0, arrayImg.shape[0], cell_size):
    for j in range(0, arrayImg.shape[1], cell_size):
        cur_block = arrayImg[i:i+cell_size, j:j+cell_size]
        griddedImage[i+(i//cell_size)*grid_size:i+(i//cell_size)*grid_size+cell_size, j+(j//cell_size)*grid_size:j+(j//cell_size)*grid_size+cell_size] = cur_block

img2 = Image.fromarray(griddedImage.astype(np.uint8))
img2.save("images/gridded_" + filename)
