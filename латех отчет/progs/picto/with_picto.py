from PIL import Image, ImageDraw, ImageFont
import numpy as np
from random import *


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

def defineCellSize(img, width=0, height=0):
    if width!=0 and height!=0:
        return min(img.width // width, img.height // height)
    elif width!=0:
        return img.width // width
    else:
        return img.height // height

def cropToWidthHeight(img, width=0, height=0):
    if width!=0 and height!=0:
        if img.width // width > img.height // height:
            fields = (img.width - img.width / ((img.width // width) / (img.height // height))) // 2
            img = img.crop((fields, 0, img.width - fields, img.height))
        else:
            fields = (img.height - img.height / ((img.height // height) / (img.width // width))) // 2
            img = img.crop((0, fields, img.width, img.height -fields))
    return img

def cropToCellSize(img, cell_size):
    cropped_width = img.width - img.width % cell_size
    cropped_height = img.height - img.height % cell_size
    img = img.crop((img.width % cell_size // 2, img.height % cell_size // 2, img.width % cell_size // 2 + cropped_width, img.height % cell_size // 2 + cropped_height))
    return img

def makePixelized(arrayImgSource, cell_size):
    #Iterate all possible cells
    for row in range(0, arrayImgSource.shape[0], cell_size):
        for col in range(0, arrayImgSource.shape[1], cell_size):
            #Get color-array for average of all colors in cell
            cur_pixel = arrayImgSource[row:row+cell_size, col:col+cell_size].sum(axis=(0,1))
            cur_pixel = cur_pixel // cell_size**2
            #Paint all pixels of cell in average color
            arrayImgSource[row:row+cell_size, col:col+cell_size] = cur_pixel
    return arrayImgSource

def generateRandomColor(arrayImgSource):
    color = np.zeros(3)
    pixel_x = randint(0, arrayImgSource.shape[0]-1)
    pixel_y = randint(0, arrayImgSource.shape[1]-1)
    for i in range (0, 3):
        color[i] = arrayImgSource[pixel_x, pixel_y, i]
    return color

def getColorDistance(c1, c2):
    return (30*(c1[0] - c2[0])**2 + 59*(c1[1] - c2[1])**2 + 11*(c1[2] - c2[2])**2)**0.5


def countPixels(arrayImgSource):
    pixel_counting = {}
    #Iterate all possible pixels
    for row in range(0, arrayImgSource.shape[0]):
        for col in range(0, arrayImgSource.shape[1]):
            cur_color_code = getColorCode(arrayImgSource[row, col])
            if cur_color_code not in pixel_counting.keys():
                pixel_counting[cur_color_code] = 1
            else:
                pixel_counting[cur_color_code] += 1
    return pixel_counting

def findKeyColors(arrayImgSource, key_colors_amount):
    pixel_counting = countPixels(arrayImgSource)
    #Get amount of key colors on result image and create an array for key colors and their frequences
    key_colors = np.zeros((key_colors_amount, 3))
    for i in range (0, key_colors_amount):
        key_colors[i] = generateRandomColor(arrayImgSource)
    key_colors_centroids = np.zeros((key_colors_amount, 3))
    key_colors_clastersize = np.zeros(key_colors_amount)

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
                key_colors_centroids[j] = generateRandomColor(arrayImgSource)
            else:
                for k in range(0, 3):
                    key_colors_centroids[j, k] = round(key_colors_centroids[j, k] / key_colors_clastersize[j])
        if (not np.array_equal(key_colors_centroids, key_colors)):
            key_colors = key_colors_centroids[::]
            key_colors_centroids = np.zeros((key_colors_amount, 3))
            key_colors_clastersize = np.zeros(key_colors_amount)
    return key_colors

def repaintWithCellStep(arrayImgSource, key_colors, cell_size):
    for row in range(0, arrayImgSource.shape[0], cell_size):
        for col in range(0, arrayImgSource.shape[1], cell_size):
            #Find the closest color from key colors
            best_color_ind = 0
            cur_color_distance = getColorDistance(key_colors[0], arrayImgSource[row, col])
            for cur_c in range (1, len(key_colors)):
                if getColorDistance(key_colors[cur_c], arrayImgSource[row, col]) < cur_color_distance:
                    cur_color_distance = getColorDistance(key_colors[cur_c], arrayImgSource[row, col])
                    best_color_ind = cur_c
            #Change cur pixel color on closest one
            arrayImgSource[row:row+cell_size, col:col+cell_size] = key_colors[best_color_ind]
    return arrayImgSource

def getCertainIntenceIndicator(color_array):
    return (color_array[0]*0.299 + color_array[1]*0.587 + color_array[2]*0.114) > 50

def getCommonIntenceIndicator(arrayImgSource):
    all_pixels = arrayImgSource.sum(axis=(0,1))
    final_pixel = all_pixels // (arrayImgSource.shape[0] * arrayImgSource.shape[1])
    return (final_pixel[0]*0.299 + final_pixel[1]*0.587 + final_pixel[2]*0.114) > 186

def findCoeffToCellSize(cell_size):
    coeff = 1
    while coeff < 15/cell_size or abs(cell_size*coeff - round(cell_size*coeff)) > 0.000001:
        coeff += 0.1
    return coeff

def stretchToNormalCellSize(img, coeff):
    img = img.resize((round(img.width*coeff), round(img.height*coeff)), Image.NEAREST)
    return img

def symbolsWithCellAndGridStep(imgWithPicto, arrayImgSource, key_colors, cell_size):
    font = ImageFont.truetype("../../CrossStitch3/crossstitch3.ttf", size=cell_size*0.8)
    alphabet = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm!@#$%^&*()[]{};:',.<>/?1234567890"
    grid_size = max(cell_size//10, 1)
    picto_field = cell_size*0.1
    for row in range(0, arrayImgSource.shape[0], cell_size + grid_size):
        for col in range(0, arrayImgSource.shape[1], cell_size + grid_size):
            for cur_c in range (0, len(key_colors)):
                if np.array_equal(key_colors[cur_c], arrayImgSource[row, col]):
                    if getCertainIntenceIndicator(arrayImgSource[row, col]):
                        picto_color=(0, 0, 0)
                    else:
                        picto_color=(128, 128, 128)
                    imgWithPicto.text((col + picto_field, row + picto_field), alphabet[cur_c], font=font, fill=picto_color)
                    break
    return imgWithPicto

def addGrid(arrayImgSource, cell_size):
    grid_size = max(cell_size//10, 1)
    cells_in_height = arrayImgSource.shape[0] // cell_size
    cells_in_width = arrayImgSource.shape[1] // cell_size
    print(cells_in_height, cells_in_width, arrayImgSource.shape[0], arrayImgSource.shape[1])
    if getCommonIntenceIndicator(arrayImgSource):
        color = 0
    else:
        color = 128
    griddedImage = np.full((arrayImgSource.shape[0] + (cells_in_height-1)*grid_size, arrayImgSource.shape[1] + (cells_in_width-1)*grid_size, 3), color)
    for i in range(0, arrayImgSource.shape[0], cell_size):
        for j in range(0, arrayImgSource.shape[1], cell_size):
            cur_block = arrayImgSource[i:i+cell_size, j:j+cell_size]
            griddedImage[i+(i//cell_size)*grid_size:i+(i//cell_size)*grid_size+cell_size, j+(j//cell_size)*grid_size:j+(j//cell_size)*grid_size+cell_size] = cur_block
    return griddedImage
    
#Get a name of image in "images" folder and read an image
filename = input()
img = Image.open("../../images/origins/" + filename)
key_colors_amount = int(input())
width_in_crosses = input()
if width_in_crosses == "":
    width_in_crosses = 0
else:
    width_in_crosses = int(width_in_crosses)
height_in_crosses = input()
if height_in_crosses == "":
    height_in_crosses = 0
else:
    height_in_crosses = int(height_in_crosses)

#Get a size of "pixels" on result image
cell_size = defineCellSize(img, width_in_crosses, height_in_crosses)
img = cropToWidthHeight(img, width_in_crosses, height_in_crosses)
img = cropToCellSize(img, cell_size)
arrayImg = np.array(img)
arrayImg.setflags(write=1)
arrayImg = makePixelized(arrayImg, cell_size)
arrayImg = arrayImg.astype(np.uint8)
key_colors = findKeyColors(arrayImg, key_colors_amount)
arrayImg = repaintWithCellStep(arrayImg, key_colors, cell_size)

coeff = findCoeffToCellSize(cell_size)
img2 = Image.fromarray(arrayImg.astype(np.uint8))
img2 = stretchToNormalCellSize(img2, coeff)
cell_size = round(coeff*cell_size)

print(cell_size, img2.width/cell_size, img2.height/cell_size)
img2 = cropToCellSize(img2, cell_size)
img2.show()
arrayImg2 = np.array(img2)
arrayImg2.setflags(write=1)


arrayImg2 = addGrid(arrayImg2, cell_size)
img3 = Image.fromarray(arrayImg2.astype(np.uint8))

imgWithPicto = ImageDraw.Draw(img3)
imgWithPicto = symbolsWithCellAndGridStep(imgWithPicto, arrayImg2, key_colors, cell_size)
              
img3.save("../../images/refactoring1/with_picto_" + filename)
