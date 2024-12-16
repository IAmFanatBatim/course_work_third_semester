from PIL import Image
import numpy as np
from random import *
 
#Get a name of image in "images" folder and read an image
filename = input()
img = Image.open("images/" + filename)
 
#Convert image object into array and open it for writing
arrayImg = np.array(img)
arrayImg.setflags(write=1)

#Create an array for number of occurrences for every color
pixel_counting = np.zeros((256, 256, 256))

#least_color = np.full(3, 255)
#most_color = np.zeros(3)

#Iterate all possible pixels
for row in range(0, arrayImg.shape[0]):
    for col in range(0, arrayImg.shape[1]):
        pixel_counting[arrayImg[row, col, 0], arrayImg[row, col, 1], arrayImg[row, col, 2]] += 1
        #for comp in range (0, 3):
            #least_color[comp] = min(least_color[comp], arrayImg[row, col, comp])
            #most_color[comp] = max(most_color[comp], arrayImg[row, col, comp])


def generateRandomColor():
    color = np.zeros(3)
    pixel_x = randint(0, arrayImg.shape[0])
    pixel_y = randint(0, arrayImg.shape[1])
    for i in range (0, 3):
        color[i] = arrayImg[pixel_x, pixel_y, i]
    return color

#print(least_color[0], most_color)
#Get amount of key colors on result image and create an array for key colors and their frequences
key_colors_amount = int(input())
key_colors = np.zeros((key_colors_amount, 3))
for i in range (0, key_colors_amount):
    key_colors[i] = generateRandomColor()
key_colors_centroids = np.zeros((key_colors_amount, 3))
key_colors_clastersize = np.zeros(key_colors_amount)


#return distance between two colors
def getColorDistance(c1, c2):
    return (30*(c1[0] - c2[0])**2 + 59*(c1[1] - c2[1])**2 + 11*(c1[2] - c2[2])**2)**0.5

#Iterate all posiible colors
#for r in range(least_color[0], most_color[0]+1):
 #   for g in range(least_color[1], most_color[1]+1):
  #      for b in range(least_color[2], most_color[2]+1):
while (not np.array_equal(key_colors_centroids, key_colors)):
    for x in range(0, arrayImg.shape[0]):
        for y in range(0, arrayImg.shape[1]):
            cur_color = np.array([arrayImg[x, y, 0], arrayImg[x, y, 1], arrayImg[x, y, 2]])
            optimal_distance = 2500
            closest_core_index = 0
            for i in range (0, key_colors_amount):
                if getColorDistance(cur_color, key_colors[i]) < optimal_distance:
                    optimal_distance = getColorDistance(cur_color, key_colors[i])
                    closest_core_index = i
            key_colors_centroids[closest_core_index] += cur_color
            key_colors_clastersize[closest_core_index] += 1
    for j in range (0, key_colors_amount):
        for k in range(0, 3):
            key_colors_centroids[j, k] = round(key_colors_centroids[j, k] / key_colors_clastersize[j])
    print(key_colors_centroids)
    print(key_colors)
    print("\n")
    
    if (not np.array_equal(key_colors_centroids, key_colors)):
        key_colors = key_colors_centroids[::]
        key_colors_centroids = np.zeros((key_colors_amount, 3))
        key_colors_clastersize = np.zeros(key_colors_amount)

print(key_colors)

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
img2.save("images/clastered_another_reduced_" + str(key_colors_amount) + "_" + filename)
