from PIL import Image
import numpy as np
 
#Get a name of image in "images" folder and read an image
filename = input()
img = Image.open("../../images/origins/" + filename)
 
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
#key_colors_frequency = np.zeros(key_colors_amount)
key_colors = np.zeros((key_colors_amount, 3))

#Defining a const for controlling an area around key colors
coeff = float(input())
all_pixels = arrayImg.shape[0]*arrayImg.shape[1]
portion = all_pixels//(key_colors_amount*coeff)

#Iterate all positions in key color array
for cur_c in range (0, key_colors_amount):
    max_color = np.zeros(3)
    max_frequency = 0
    #Iterate all posiible colors
    for r in range(0, 256):
        for g in range(0, 256):
            for b in range(0, 256):
                #Rewrite max color value if its frequence more than current one
                if pixel_counting[r, g, b] > max_frequency:
                    max_frequency = pixel_counting[r, g, b]
                    max_color = [r, g, b]
    #insert max color in key colors on current position
    key_colors[cur_c] = max_color
    #Set a size of area around max color for erasing
    rad = 0
    #Set a variable for max color components and arrays for borders
    cr = int(max_color[0])
    cg = int(max_color[1])
    cb = int(max_color[2])
    left_borders = [cr, cg, cb]
    right_borders = [cr, cg, cb]

    #Continue until area not equal all array
    while left_borders[0] != 0 or left_borders[1] != 0 or left_borders[2] != 0 or right_borders[0] != 0 or right_borders[1] != 0 or right_borders[2] != 0:
        #Get a indexs of borders so they don't outline array borders
        left_borders = [max(0, cr-rad), max(0, cg-rad), max(0, cb-rad)]
        right_borders = [min(255, cr+rad), min(255, cg+rad), min(255, cb+rad)]
        cur_sum = pixel_counting[left_borders[0]:right_borders[0]+1, left_borders[1]:right_borders[1]+1, left_borders[2]:right_borders[2]+1].sum()
        if cur_sum > portion:
            #Decrease the size of area and erase data about color inside this area
            rad-=1
            left_borders = [max(0, cr-rad), max(0, cg-rad), max(0, cb-rad)]
            right_borders = [min(255, cr+rad), min(255, cg+rad), min(255, cb+rad)] 
            pixel_counting[left_borders[0]:right_borders[0]+1, left_borders[1]:right_borders[1]+1, left_borders[2]:right_borders[2]+1] = 0
            break
        #Increase the size of area
        rad += 1

print(key_colors)

#return distance between two colors
def getColorDistance(c1, c2):
    return (30*(c1[0] - c2[0])**2 + 59*(c1[1] - c2[1])**2 + 11*(c1[2] - c2[2])**2)**0.5

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
img2.save("../../images/reduced/reduced_with_step_" + str(key_colors_amount) + "_" + str(coeff) + "_" + filename)
