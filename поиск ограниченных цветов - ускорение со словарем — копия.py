from PIL import Image
import numpy as np

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

print(tohex(9))
print(tohex(16))
print(tohex(256))
print(tohex(145))
print(tohex(235))


print(fromhex("9"))
print(fromhex("10"))
print(fromhex("100"))
print(fromhex("EB"))


def getColorCode(color_array):
    codeparts = [tohex(color_array[0]), tohex(color_array[1]), tohex(color_array[2])]
    for i in range (0, len(codeparts)):
        while len(codeparts[i]) < 2:
            codeparts[i] = "0" + codeparts[i]
    return codeparts[0] + codeparts[1] + codeparts[2]
print(getColorCode([9, 145, 235]))

def getColorArray(hexcode):
    return [fromhex(hexcode[0:2]), fromhex(hexcode[2:4]), fromhex(hexcode[4:6])]
print(getColorArray("0991EB"))


# read an image
img = Image.open('cats.jpg')
 
# convert image object into array
imageToMatrice = np.array(img)
imageToMatrice.setflags(write=1)


cell_size = 5

pixel_counting = {}

for i in range(0, imageToMatrice.shape[0]):
    for j in range(0, imageToMatrice.shape[1]):
        cur_color_code = getColorCode(imageToMatrice[i, j])
        if cur_color_code not in pixel_counting.keys():
            pixel_counting[cur_color_code] = 1
        else:
            pixel_counting[cur_color_code] += 1

counter_of_zeros = 0

#for i in range(0, 256, 14):
#    for j in range(0, 256, 14):
#        for k in range(0, 256, 14):
#            code = getColorCode([i, j, k])
#            if code not in pixel_counting.keys():
#                counter_of_zeros += 1
#            else:
#                if (counter_of_zeros != 0):
#                    print("0 *", counter_of_zeros)
#                print(pixel_counting[code])
#                counter_of_zeros = 0




#print(pixel_counting.keys())
key_colors_amount = 20
key_colors_frequency = np.zeros(key_colors_amount)
key_colors = np.zeros((key_colors_amount, 3))

for i in pixel_counting.keys():
    cur_color_array = getColorArray(i)
    #print(i, pixel_counting[i], cur_color_array)
    for l in range (0, key_colors_amount):
        if pixel_counting[i] > key_colors_frequency[l]:
            key_colors_frequency[l+1:key_colors_amount] = key_colors_frequency[l:key_colors_amount-1]
            key_colors_frequency[l] = pixel_counting[i]
            key_colors[l+1:key_colors_amount] = key_colors[l:key_colors_amount-1]
            key_colors[l] = cur_color_array
            #print(i, pixel_counting[i], cur_color_array)
            break
print(key_colors)
print(key_colors_frequency)                

def getColorDistance(c1, c2):
    return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)**0.5

for i in range(0, imageToMatrice.shape[0]):
    for j in range(0, imageToMatrice.shape[1]):
        best_color_ind = 0
        cur_color_distance = getColorDistance(key_colors[0], imageToMatrice[i, j])
        for k in range (1, key_colors_amount):
            if getColorDistance(key_colors[k], imageToMatrice[i, j]) < cur_color_distance:
                cur_color_distance = getColorDistance(key_colors[k], imageToMatrice[i, j])
                best_color_ind = k
        imageToMatrice[i, j] = key_colors[best_color_ind]

img2 = Image.fromarray(imageToMatrice)
img2.save('poor_cats_2.jpg')
