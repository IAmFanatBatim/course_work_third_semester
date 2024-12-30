#A library for wirking with JSON files
import json

#Open a text file with data about DMC threads
data = open("DMC data.txt", "r")
#Split it into lines of certain colors
all_strings = data.readlines()
#Create an array for dicts
array_of_threads = []
#Iterate all lines of colors
for cur_string in all_strings:
    #Split current string into parameters
    parameters = cur_string.split("\t")
    #Create a current dict and fill in with key-value pairs
    cur_thread = {}
    cur_thread["thread_code"] = parameters[0]
    cur_thread["thread_name"] = parameters[1]
    cur_thread["thread_HEX_code"] = parameters[2]
    cur_thread["thread_RGB"] = (int(parameters[3]), int(parameters[4]), int(parameters[5]))
    #Add it in array of dicts
    array_of_threads.append(cur_thread)
#Create JSON-file and dumping array of dicts
with open("DMC data.json", "w") as json_file:
    json.dump(array_of_threads, json_file, indent=4)
