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

#least_color = np.full(3, 255)
#most_color = np.zeros(3)

#Iterate all possible pixels
for row in range(0, arrayImg.shape[0]):
    for col in range(0, arrayImg.shape[1]):
        pixel_counting[arrayImg[row, col, 0], arrayImg[row, col, 1], arrayImg[row, col, 2]] += 1
        #for comp in range (0, 3):
            #least_color[comp] = min(least_color[comp], arrayImg[row, col, comp])
            #most_color[comp] = max(most_color[comp], arrayImg[row, col, comp])

#print(least_color[0], most_color)
#Get amount of key colors on result image and create an array for key colors and their frequences
key_colors_amount = int(input())
#key_colors_frequency = np.zeros(key_colors_amount)
key_colors = np.zeros((key_colors_amount, 3))

all_pixels = arrayImg.shape[0]*arrayImg.shape[1]
portion = all_pixels//(key_colors_amount*2)

#Iterate all posiible colors
#for r in range(least_color[0], most_color[0]+1):
 #   for g in range(least_color[1], most_color[1]+1):
  #      for b in range(least_color[2], most_color[2]+1):
for cur_c in range (0, key_colors_amount):
    max_color = np.zeros(3)
    max_frequency = 0
    for r in range(0, 256):
        for g in range(0, 256):
            for b in range(0, 256):
                #Checr can current color be one of more frequent
                if pixel_counting[r, g, b] > max_frequency:
                    max_frequency = pixel_counting[r, g, b]
                    max_color = [r, g, b]
    key_colors[cur_c] = max_color
    sq_rad = 1
    print(max_color[0])
    cr = int(max_color[0])
    cg = int(max_color[1])
    cb = int(max_color[2])
    while (cr - sq_rad >= 0 and cr + sq_rad <= 255) and (cg - sq_rad >= 0 and cg + sq_rad <= 255) and (cb - sq_rad >= 0 and cb + sq_rad <= 255):
        print("here")
        cur_sum = pixel_counting[cr-sq_rad:cr+sq_rad+1, cg-sq_rad:cg+sq_rad+1, cb-sq_rad:cb+sq_rad+1].sum()
        if cur_sum > portion:
            sq_rad-=1
            print((cr*256 + cg)*256 + cb)
            #Add this color, shift others and come to next color                        
            break
        sq_rad+=1
    pixel_counting[cr-sq_rad:cr+sq_rad+1, cg-sq_rad:cg+sq_rad+1, cb-sq_rad:cb+sq_rad+1] = 0


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
img2.save("images/third_reduced_" + str(key_colors_amount) + "_" + filename)
