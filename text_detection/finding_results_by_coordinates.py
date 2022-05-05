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


result = OCR_TD(r'C:\Users\tayeb\Desktop\New folder\training\1.jpg')
print(result)


def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def coordinates(result):
    for x in result:
        file = open('expiry_date.txt', 'r')
        if result[x][1] in file.read():
            exp_string = result[x][1]
            exp_string = exp_string.split(":")[0]
            if is_date(exp_string):
                return exp_string
            else:
                Xb = result[0][1][0]
                Yb = result[0][1][1]
