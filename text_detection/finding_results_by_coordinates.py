import easyocr
import os
import cv2
from matplotlib import pyplot as plt
import regex
import numpy as np
from dateutil.parser import parse


def OCR_TD(IMAGE_PATH):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(IMAGE_PATH, decoder='greedy', batch_size=50,width_ths=12)
    return result



def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def coordinates(result):
    average = 1000000
    x = 0
    x1 = 0
    for z in result:
        file = open('expiry_date.txt', 'r')
        if result[x][1] in file.read():
            print(result[x][1])
            exp_string = result[x][1]
            exp_string = exp_string.split(":")[0]
            if is_date(exp_string):
                exp_string = parse(exp_string)
                print(exp_string)
                return exp_string
            else:
                Xb = result[x][0][1][0]
                Yb = result[x][0][1][1]
                for z1 in result:
                    Xtemp = Xb - result[x1][0][0][0]
                    Ytemp = Yb - result[x1][0][0][1]
                    average_temp = (Xtemp + Ytemp)/2
                    print(Xtemp,Ytemp,Xb,Yb,average_temp,average)
                    if average_temp < average:
                        average = average_temp
                        Xa = Xtemp
                        Ya = Ytemp
                    x1 = x1 + 1
                x1 = 0
                for z2 in result:
                    if ((result[x1][0][0][0] == Xa) and (result[x][0][0][1] == Ya)):
                        exp_string = parse(result[x][1])
                        print(exp_string)
                        return exp_string
                    x1 = x1 + 1
        x = x + 1

def image_show(result,IMAGE_PATH):
    img = cv2.imread(IMAGE_PATH)
    top_left = tuple(result[0][0][0])
    bottom_right = tuple(result[0][0][2])
    text = result[0][1]
    for detection in result:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        text = detection[1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 5)
        img = cv2.putText(img, text, top_left, font, .5, (255, 255, 255), 2, cv2.LINE_AA)
    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.show()

image_path = r'C:\Users\tayeb\Desktop\New folder\training\29.jpg'
result = OCR_TD(image_path)
print(coordinates(result))
image_show(result,image_path)
