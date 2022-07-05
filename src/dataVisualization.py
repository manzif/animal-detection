import os
from os import walk, getcwd
import numpy as np
import cv2

classes = [
        'giraffe',
        'person',
        'zebra',
        'elephant',
        'impala',
        'monkey',
        'lion',
        'leopard',
        'crocodile',
        'buffalo',
        'hyna',
        'bird',
        'gorilla'
        ]
        
def convert(size,x,y,w,h):
    box = np.zeros(4)
    dw = 1./size[0]
    dh = 1./size[1]
    x = x/dw
    w = w/dw
    y = y/dh
    h = h/dh
    box[0] = x-(w/2.0)
    box[1] = x+(w/2.0)
    box[2] = y-(h/2.0)
    box[3] = y+(h/2.0)

    return (box)
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
mypath_txt = "../datasets/annotations_txt/"
mypath_images = "../datasets/images/"
outpath = "../datasets/images_lebels/"

wd = getcwd()

""" Get yolo txt file list """
txt_list = []
for file in os.listdir(mypath_txt):
    if file.endswith(".txt"):
        txt_list.append(file)
    

""" Process """
for txt_name in txt_list:
    img_filename = txt_name.rstrip(".txt") + ".jpg"
    img_path = mypath_images + txt_name.rstrip(".txt") + ".jpg"
    img = cv2.imread(img_path)

    """ Open input text files """
    txt_path = mypath_txt + txt_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    
    img_outpath = outpath + img_filename
    print("Output:" + img_outpath)

    """ Convert YOLO format to get xmin,ymin,xmax,ymax """ 
    lines = txt_file.read().splitlines() 
    #print(lines) 
    for idx, line in enumerate(lines):
        
        value = line.split()
        
        x=y=w=h=cls= None
        cls = value[0]
        #print(cls)
        x = float(value[1])
        y = float(value[2])
        w = float(value[3])
        h = float(value[4])

        # Getting images size
        img_h, img_w = img.shape[:2]

        # Getting bounding box in the image coordinates
        bb = convert((img_w, img_h), x,y,w,h)
        if cls==str(0):
            color = (0, 0, 255)
        elif cls==str(1):
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        
        # Drawing the bounding box
        cv2.rectangle(img, (int(round(bb[0])),int(round(bb[2]))),(int(round(bb[1])),int(round(bb[3]))),color,2)

        # Writing class names
        cv2.putText(img, classes[int(cls)], (int(round(bb[0])),int(round(bb[2]))), cv2.FONT_HERSHEY_SIMPLEX,1, (209, 80, 0, 255),  3) 
        
        cv2.imwrite(img_outpath, img)