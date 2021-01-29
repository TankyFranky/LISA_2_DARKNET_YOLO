# Francesco Marrato
# 2021-01-28

import os
import glob
import csv
from PIL import Image

"""
Script built to convert the LISA Traffic Sign data set from the .csv format into the darknet/YOLO .txt format for training using LISA data.

Works off a per file folder basis, will generate multiple identical obj.data and obj.names files that will have to be removed (leave 1)
Use the supplied categories.txt file as the one included with the LISA dataset does not include all the categories

If used please reference its use:

Francesco Marrato, 2021-01-29, Queen's University Department of Electrical and Computer Engineering

"""

# Root address including folder name (use / not \)
input_folder_location = "F:/Queens/Comp_Eng_2020-2021/Capstone Project/signDatabasePublicFramesOnly/vid5/frameAnnotations-vid_cmp2.avi_annotations/"
input_classfile_location = "F:/Queens/Comp_Eng_2020-2021/Capstone Project/signDatabasePublicFramesOnly/categories.txt" # Use categories.txt from Git as it includes stop and yield
output_folder_location = "F:/Queens/Comp_Eng_2020-2021/Capstone Project/LISA_2_YOLO/LISA_2_YOLO/Video5/" # Don't forget a / at the end


# store info in dictionary so it can be manipulated easily
processing_dictionary = {}
category_dictionary = {}

# parse the categories.txt file into a dictionary
# create the obj.names file with the dictionary
with open(input_classfile_location,'r') as categories_reader:
    categories = categories_reader.read().replace('\n','').replace(' ','')
    categories = categories.split(',')
    obj_names = open(output_folder_location + "obj.names", "w")
    for val, type in enumerate(categories):
        category_dictionary[type] = val
        obj_names.write(type + "\n")
    obj_names.close()

# create obj.data file with the dictionary
    obj_data = open(output_folder_location + "obj.data", "w")
    obj_data.write("classes = " + str(len(category_dictionary)) + "\ntrain = data / train.txt\nvalid = data / test.txt\nnames = data / obj.names\nbackup = backup / ")
    obj_data.close()

# convert .png images to .jpg, skip the csv file
for file_name in os.listdir(input_folder_location):
    try:
        new_name = os.path.splitext(file_name)[0]
        jpg_save = Image.open(input_folder_location + file_name).convert("RGB")
        jpg_save.save(output_folder_location + new_name + ".jpg", "jpeg")
    except:
        print("cannot covert file: " + file_name)

# open the csv file
path_2_csv = input_folder_location +"*.csv"
csv_file = glob.glob(path_2_csv)

with open(csv_file[0],'r') as csv_reader:
    next(csv_reader, None)
    csv_obj = csv.reader(csv_reader, delimiter=",")
    for row in csv_obj:
        info = row[0].split(";")
        img_data = Image.open(input_folder_location + info[0])
        width, height = img_data.size
        file_name = info[0].replace('.png','.jpg')

        type = category_dictionary[info[1]] # type is the number in reference to the dictionary
        xWidth = (int(info[4]) - int(info[2]))/width    # width of the surrounding square as a ratio of the image
        yWidth = (int(info[5]) - int(info[3]))/height   # height of the surrounding square as a ratio of the image
        xPos =  ((xWidth/2) + int(info[2]))/width   # center position (x) of the surrounding square as a ratio of the image
        yPos =  ((yWidth/2) + int(info[3]))/height  # center position (x) of the surrounding square as a ratio of the image

        dict_entry = [type,xPos,yPos,xWidth,yWidth]

        if file_name in processing_dictionary:
            processing_dictionary[file_name].append(dict_entry) # add another instance of class
        else:
            processing_dictionary[file_name] = [dict_entry] # create new entry in dictionary


# Save the dictionary entries to the appropriate txt files
for entry, signs  in processing_dictionary.items():
    yolo_txt_file = open(output_folder_location + str(entry.replace(".jpg",".txt")), "w")
    for each in signs:
        yolo_txt_file.write(str(each[0]) + " " + str(each[1]) + " " + str(each[2]) + " " + str(each[3]) + " " + str(each[4]) + "\n")
    yolo_txt_file.close()
