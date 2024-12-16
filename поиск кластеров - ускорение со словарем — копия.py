from PIL import Image
import numpy as np

img = Image.open('cats.jpg')
 
# convert image object into array
imageToMatrice = np.array(img)
imageToMatrice.setflags(write=1)

conturs = np.full((imageToMatrice.shape[0], imageToMatrice.shape[1], 3), 255)
#img15 = Image.fromarray((conturs).astype(np.uint8)).convert('RGB')
#img15.save('divided_cats.jpg')



def getColorDistance(c1, c2):
    return int((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)**0.5

for i in range(1, imageToMatrice.shape[0]-1):
    for j in range(1, imageToMatrice.shape[1]-1):
        cur_square = imageToMatrice[i-1:i+2, j-1:j+2]
        #print(cur_square, "\n\n")
        #print(imageToMatrice[i, j])
        for cur_bit in range(0, 9):
            cur_bit_x = cur_bit % 3
            cur_bit_y = cur_bit // 3
            #print(getColorDistance(imageToMatrice[i, j], cur_square[cur_bit_x, cur_bit_y]))
            if getColorDistance(imageToMatrice[i, j], cur_square[cur_bit_x, cur_bit_y]) > 15:
                conturs[i + cur_bit_x-1, j+cur_bit_y-1] = (0, 0, 0)
            

img2 = Image.fromarray((conturs).astype(np.uint8)).convert('RGB')
img2.save('divided_cats.jpg')
