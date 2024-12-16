from PIL import Image
import numpy as np
 
#Get a name of image in "images" folder and read an image
filename = input()
img = Image.open("images/" + filename)
 
#Convert image object into array and open it for writing
arrayImg = np.array(img)
arrayImg.setflags(write=1)

#Create an array for number of occurrences for every color
pixel_counting = np.zeros((256, 256, 256))

#Iterate all possible pixels
for row in range(0, arrayImg.shape[0]):
    for col in range(0, arrayImg.shape[1]):
        pixel_counting[arrayImg[row, col, 0], arrayImg[row, col, 1], arrayImg[row, col, 2]] += 1

#Get amount of key colors on result image and create an array for key colors and their frequences
key_colors_amount = int(input())
key_colors_frequency = np.zeros(key_colors_amount)
key_colors = np.zeros((key_colors_amount, 3))

#Iterate all posiible colors
for r in range(0, 256):
    for g in range(0, 256):
        for b in range(0, 256):
            #Checr can current color be one of more frequent
            if (pixel_counting[r, g, b] > key_colors_frequency[key_colors_amount-1]):
                #Search a place in array for this color
                for cur_c in range (0, key_colors_amount):
                    if pixel_counting[r, g, b] > key_colors_frequency[cur_c]:
                        #Add this color, shift others and come to next color
                        key_colors_frequency[cur_c+1:key_colors_amount] = key_colors_frequency[cur_c:key_colors_amount-1]
                        key_colors_frequency[cur_c] = pixel_counting[r, g, b]
                        key_colors[cur_c+1:key_colors_amount] = key_colors[cur_c:key_colors_amount-1]
                        key_colors[cur_c] = [r, g, b]
                        break

#return distance between two colors
def getColorDistance(c1, c2):
    return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)**0.5

#Iterate all possible pixels
for row in range(0, arrayImg.shape[0]):
    for col in range(0, arrayImg.shape[1]):
        #Find the closest color from key colors
        best_color_ind = 0
        cur_color_distance = getColorDistance(key_colors[0], arrayImg[row, col])
        for cur_c in range (1, key_colors_amount):
            if getColorDistance(key_colors[cur_c], arrayImg[row, col]) < cur_color_distance:
                cur_color_distance = getColorDistance(key_colors[cur_c], arrayImg[row, col])
                best_color_ind = cur_c
        #Change cur pixel color on closest one
        arrayImg[row, col] = key_colors[best_color_ind]

#Convert array into image object and save it in same folder
img2 = Image.fromarray(arrayImg)
img2.save("images/reduced_" + filename)
