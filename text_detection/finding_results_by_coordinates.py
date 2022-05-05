import easyocr
import os
import cv2
from matplotlib import pyplot as plt
import regex
import numpy as np
from dateutil.parser import parse


def OCR_TD(IMAGE_PATH):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(IMAGE_PATH, decoder='greedy', batch_size=50)
    return result



def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def coordinates(result):
    average = 1000000
    for x in result:
        file = open('expiry_date.txt', 'r')
        if file.read() in result[x][1]:
            exp_string = result[x][1]
            exp_string = exp_string.split(":")[0]
            if is_date(exp_string):
                exp_string = parse(exp_string)
                return exp_string
            else:
                Xb = result[x][0][1][0]
                Yb = result[x][0][1][1]
                for x in result:
                    Xtemp = Xb - result[x][0][1][0]
                    Ytemp = Yb - result[x][0][1][1]
                    average_temp = (Xtemp + Ytemp)/2
                    if average_temp < average:
                        average = average_temp
                        Xa = Xtemp
                        Ya = Ytemp
                for x in result:
                    if ((result[x][0][1][0] == Xa) and (result[x][0][1][1] == Ya)):
                        exp_string = parse(result[x][1])
                        return exp_string



result = OCR_TD(r'C:\Users\tayeb\Desktop\New folder\training\1.jpg')
print(coordinates(result))