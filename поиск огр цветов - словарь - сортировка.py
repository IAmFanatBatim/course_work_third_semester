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

def getColorCode(color_array):
    codeparts = [tohex(color_array[0]), tohex(color_array[1]), tohex(color_array[2])]
    for i in range (0, len(codeparts)):
        while len(codeparts[i]) < 2:
            codeparts[i] = "0" + codeparts[i]
    return codeparts[0] + codeparts[1] + codeparts[2]

def getColorArray(hexcode):
    return [fromhex(hexcode[0:2]), fromhex(hexcode[2:4]), fromhex(hexcode[4:6])]

def quickSort(array, l, r, f):
    reference_ind = l
    left_ind = l
    right_ind = r
    while (left_ind <= right_ind):
        while f(array[left_ind], array[reference_ind]) == -1 and left_ind <= r:
            left_ind += 1
        while f(array[right_ind], array[reference_ind]) == 1 and right_ind >= l:
            right_ind -= 1
        if (left_ind <= right_ind):
            array[left_ind], array[right_ind] = array[right_ind], array[left_ind]
            left_ind += 1
            right_ind -= 1
    if (right_ind > l):
        array = quickSort(array, l, right_ind, f);
    if (left_ind < r):
        array = quickSort(array, left_ind, r, f);
    return array

def compare_frequency(color_note_1, color_note_2):
    first = color_note_1.get('frequency', 0)
    second = color_note_2.get('frequency', 0)
    if first > second:
        return -1
    elif first < second:
        return 1
    else:
        return 0

def addLocalNeigbours(color_array, zone, cur_code, direction):
    for i in range(0, 6, 2):
        print(cur_code[i:i+2])
        if cur_code[i:i+2] != "00":
            col_ar = getColorArray(cur_code)
            col_ar[i//2] -= 1
            col_co = getColorCode(col_ar)
            print(col_co)
            if col_co in color_array.keys():
                if direction[i//2] != -1 and col_co not in zone:
                    zone.append(col_co)
            elif direction[i//2] != -1:
                #print([0]*(i//2) + [1] + [0]*((4-i)//2))
                zone = addLocalNeigbours(color_array, zone, col_co, [0]*(i//2) + [1] + [0]*((4-i)//2))
        if cur_code[i:i+2] != "FF":
            col_ar = getColorArray(cur_code)
            col_ar[i//2] += 1
            col_co = getColorCode(col_ar)
            print(col_co)
            if col_co in color_array.keys():
                if direction[i//2] != 1 and col_co not in zone:
                    zone.append(col_co)
            elif direction[i//2] != 1:
                zone = addLocalNeigbours(color_array, zone, col_co, [0]*(i//2) + [-1] + [0]*((4-i)//2))  
    return zone

def isLocalPeak(color_array, cur_code):
    zone = addLocalNeigbours(color_array, [], cur_code, (0, 0, 0))
    for c in zone:
        if color_array[c] > color_array[cur_code]:
            return 0
    return 1


#def isLocalPeak(color_array, cur_code):
#    for i in range(0, 6, 2):
#        if cur_code[i:i+2] != "00":
#            col_ar = getColorArray(cur_code)
#            col_ar[i//2] -= 1
#            col_co = getColorCode(col_ar)
#            if col_co in color_array.keys():
#                if color_array[col_co] > color_array[cur_code]:
#                    return 0
#        if cur_code[i:i+2] != "FF":
#            col_ar = getColorArray(cur_code)
#            col_ar[i//2] += 1
#            col_co = getColorCode(col_ar)
#            if col_co in color_array.keys():
#                if color_array[col_co] > color_array[cur_code]:
#                    return 0
#    return 1

# read an image
img = Image.open('cats.jpg')
 
# convert image object into array
imageToMatrice = np.array(img)
imageToMatrice.setflags(write=1)

pixel_counting_dict = {}

for i in range(0, imageToMatrice.shape[0]):
    for j in range(0, imageToMatrice.shape[1]):
        cur_color_code = getColorCode(imageToMatrice[i, j])
        if cur_color_code not in pixel_counting_dict.keys():
            pixel_counting_dict[cur_color_code] = 1
        else:
            pixel_counting_dict[cur_color_code] += 1

pixel_counting = []
print(len(pixel_counting_dict.keys()))
for i in pixel_counting_dict.keys():
    if isLocalPeak(pixel_counting_dict, i):
        cur_note = {"color_code": i, "frequency": pixel_counting_dict[i]}
        pixel_counting.append(cur_note)

pixel_counting = quickSort(pixel_counting, 0, len(pixel_counting)-1, compare_frequency)
print(len(pixel_counting))
for i in range(0, 100):
    print(i, pixel_counting[i])

#print(pixel_counting.keys())
key_colors_amount = 20
key_colors_distances = np.zeros(key_colors_amount)
key_colors_distances[0] = 450
key_colors = np.zeros((key_colors_amount, 3))
key_colors[0] = getColorArray(pixel_counting[0]["color_code"])

def getColorDistance(c1, c2):
    return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)**0.5

gen_i = 1
while gen_i < len(pixel_counting):
    cur_note = pixel_counting[gen_i]
    cur_color_array = getColorArray(cur_note["color_code"])
    min_distance = 450
    for conquer_note in pixel_counting[gen_i-1::-1]:
        conquer_color_array = getColorArray(conquer_note["color_code"])
        min_distance = min(getColorDistance(cur_color_array, conquer_color_array), min_distance)
        #print(cur_color_array, conquer_color_array, min_distance)
        if min_distance == 1:
            break
    if min_distance > key_colors_distances[key_colors_amount-1]:
        for k in range (1, key_colors_amount):
            if min_distance > key_colors_distances[k]:
                key_colors_distances[1+k:key_colors_amount] = key_colors_distances[k:key_colors_amount-1]
                key_colors_distances[k] = min_distance
                key_colors[1+k:key_colors_amount] = key_colors[k:key_colors_amount-1]
                key_colors[k] = cur_color_array
                break
    gen_i += 1
print(key_colors)
print(key_colors_distances)                

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
img2.save('poor_cats.jpg')
