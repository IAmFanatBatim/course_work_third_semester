from PIL import Image
import numpy as np
from random import *
 
#Get a name of image in "images" folder and read an image
def tohex (num):
    hexstr = ""
    add_letters = "ABCDEF"
    while num > 0:
        if num % 16 >= 10:
            hexstr = add_letters[(num % 16) - 10] + hexstr
        else:
            hexstr = str(num % 16) + hexstr
        num = num // 16
    return hexstr

def fromhex (hexstr):
    num = 0
    all_letters = "0123456789ABCDEF"
    for i in range(0, len(hexstr)):
        num = num*16 + all_letters.index(hexstr[i])
    return num

def getColorCode(color_array):
    codeparts = [tohex(color_array[0]), tohex(color_array[1]), tohex(color_array[2])]
    for i in range (0, len(codeparts)):
        while len(codeparts[i]) < 2:
            codeparts[i] = "0" + codeparts[i]
    return codeparts[0] + codeparts[1] + codeparts[2]

def getColorArray(hexcode):
    return np.array([fromhex(hexcode[0:2]), fromhex(hexcode[2:4]), fromhex(hexcode[4:6])])

filename = input()
img = Image.open("../../images/" + filename)
 
#Convert image object into array and open it for writing
arrayImg = np.array(img)
arrayImg.setflags(write=1)

#Create an array for number of occurrences for every color
pixel_counting = {}

#least_color = np.full(3, 255)
#most_color = np.zeros(3)

#Iterate all possible pixels
for row in range(0, arrayImg.shape[0]):
    for col in range(0, arrayImg.shape[1]):
        cur_color_code = getColorCode(arrayImg[row, col])
        if cur_color_code not in pixel_counting.keys():
            pixel_counting[cur_color_code] = 1
        else:
            pixel_counting[cur_color_code] += 1


def generateRandomColor():
    color = np.zeros(3)
    pixel_x = randint(0, arrayImg.shape[0]-1)
    pixel_y = randint(0, arrayImg.shape[1]-1)
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
while (not np.array_equal(key_colors_centroids, key_colors)):
    for cur_hex_code in pixel_counting.keys():
        cur_color = getColorArray(cur_hex_code)
        optimal_distance = 2500
        closest_core_index = 0
        for i in range (0, key_colors_amount):
            if getColorDistance(cur_color, key_colors[i]) < optimal_distance:
                optimal_distance = getColorDistance(cur_color, key_colors[i])
                closest_core_index = i

        key_colors_centroids[closest_core_index] += cur_color * pixel_counting[cur_hex_code]
        key_colors_clastersize[closest_core_index] += pixel_counting[cur_hex_code]
    for j in range (0, key_colors_amount):
        if key_colors_clastersize[j] == 0:
            key_colors_centroids = generateRandomColor()
        for k in range(0, 3):
            key_colors_centroids[j, k] = round(key_colors_centroids[j, k] / key_colors_clastersize[j])
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
img2.save("../../images/HEXcode_clastered_reduced_" + str(key_colors_amount) + "_" + filename)
