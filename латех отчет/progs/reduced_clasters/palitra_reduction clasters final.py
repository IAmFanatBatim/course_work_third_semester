from PIL import Image
import numpy as np
from random import *
 
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

#Return a color of random pixel from arrayImg      
def generateRandomColor():
    color = np.zeros(3)
    pixel_x = randint(0, arrayImg.shape[0])
    pixel_y = randint(0, arrayImg.shape[1])
    for i in range (0, 3):
        color[i] = arrayImg[pixel_x, pixel_y, i]
    return color

#Get amount of key colors on result image
key_colors_amount = int(input())
#Create an array for key colors and fill it with random colors
key_colors = np.zeros((key_colors_amount, 3))
for i in range (0, key_colors_amount):
    key_colors[i] = generateRandomColor()
#Create an array for centes of current clasters and an array for sizes of claters and fill it with zeros 
key_colors_centroids = np.zeros((key_colors_amount, 3))
key_colors_clastersize = np.zeros(key_colors_amount)

#Teturn distance between two colors
def getColorDistance(c1, c2):
    return (30*(c1[0] - c2[0])**2 + 59*(c1[1] - c2[1])**2 + 11*(c1[2] - c2[2])**2)**0.5

#Do until arrays of key colors and centroids will be equal
while (not np.array_equal(key_colors_centroids, key_colors)):
    #Iterate all colors
    for r in range(0, 256):
        for g in range(0, 256):
            for b in range(0, 256):
                cur_color = np.array([r, g, b])
                #If this color in image, find a cluster to relate
                if pixel_counting[r, g, b] != 0:
                    optimal_distance = 2500
                    closest_core_index = 0
                    for i in range (0, key_colors_amount):
                        if getColorDistance(cur_color, key_colors[i]) < optimal_distance:
                            optimal_distance = getColorDistance(cur_color, key_colors[i])
                            closest_core_index = i
                    #Change sum of metrics and amount of points in cluster
                    key_colors_centroids[closest_core_index] += cur_color * pixel_counting[r, g, b]
                    key_colors_clastersize[closest_core_index] += pixel_counting[r, g, b]
    #Iterate all clusters: if cluster is empty, find a new center for it, else find a center as average from sum of metrics
    for j in range (0, key_colors_amount):
        if key_colors_clastersize[j] == 0:
            key_colors_centroids[j] = generateRandomColor()
        else:
            for k in range(0, 3):
                key_colors_centroids[j, k] = round(key_colors_centroids[j, k] / key_colors_clastersize[j])

    #If it's necessary, values of centroids array become values of key colors array, data about centroids and cluster size erase
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
img2.save("../../images/reduced_clasters/K-means_reduced_" + str(key_colors_amount) + "_" + filename)
