from PIL import Image
import numpy as np
 
# read an image
img = Image.open('baloons.jpg')
 
cell_size = 10
grid_size = cell_size//10

cells_in_width = img.width // cell_size
cells_in_height = img.height // cell_size

cropped_width = img.width - img.width % cell_size
cropped_height = img.height - img.height % cell_size

img = img.crop((img.width % cell_size // 2, img.height % cell_size // 2, img.width % cell_size // 2 + cropped_width, img.height % cell_size // 2 + cropped_height))

imageToMatrice = np.array(img)
imageToMatrice.setflags(write=1)

griddedImage = np.zeros((cropped_height + (cells_in_height-1)*grid_size, cropped_width + (cells_in_width-1)*grid_size, 3))

print(imageToMatrice.shape)
print(griddedImage.shape)

for i in range(0, imageToMatrice.shape[0], cell_size):
    for j in range(0, imageToMatrice.shape[1], cell_size):
        cur_block = np.zeros(3)
        for k in range(0, cell_size):
            for l in range(0, cell_size):
                cur_block = cur_block + imageToMatrice[i+k, j+l]
        cur_block = cur_block // cell_size**2
        griddedImage[i+(i//cell_size)*grid_size:i+(i//cell_size)*grid_size+cell_size, j+(j//cell_size)*grid_size:j+(j//cell_size)*grid_size+cell_size] = cur_block

img2 = Image.fromarray(griddedImage.astype(np.uint8))
img2.save('crossed_pixel_baloons.png')
