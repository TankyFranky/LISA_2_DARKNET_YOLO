# LISA_2_DARKNET_YOLO
A script for converting the LISA traffic sign dataset into YOLO/Darknet format. Works off a per folder basis, creating obj.data and obj.names files as well. Uses a custom categories.txt.

# INFO

Script built to convert the LISA Traffic Sign data set from the .csv format into the darknet/YOLO .txt format for training using LISA data.

Works off a per file folder basis, will generate multiple identical obj.data and obj.names files that will have to be removed (leave 1)
Use the supplied categories.txt file as the one included with the LISA dataset does not include all the categories

If used please reference its use:

Francesco Marrato, 2021-01-29, Queen's University Department of Electrical and Computer Engineering

Code is fully commented for easy walkthrough.

Results will output like the following.

# Example
### Input from LISA dataset
![Input](https://i.imgur.com/w9nNg3w.png)
### Output in YOLO/Darknet Format
![Result](https://i.imgur.com/IY84iaK.png)
