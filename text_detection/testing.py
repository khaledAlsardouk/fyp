import easyocr
import os
import cv2
from matplotlib import pyplot as plt
import regex
import re
import numpy as np

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

directory = r'C:\Users\khale\Desktop\fyp\test-STUFF\dataset-dates\training'
counter = 0
reader = easyocr.Reader(['en'])
dirlist = sorted_alphanumeric(os.listdir(directory))

for filename in dirlist:
    if filename.endswith(".jpg"):
        IMAGE_PATH = os.path.join(directory,filename)
        result = reader.readtext(IMAGE_PATH,decoder='wordbeamsearch',batch_size=50)
        result1 = []
        result2 = []
        result3 = []
        final_result = ''

        for text in result:
            pattern = regex.find_date_true(text[1])
            if (pattern is not None):
                result1.append(pattern)
            pattern = regex.find_date_test_CMP1(text[1])
            if (pattern is not None):
                result2.append(pattern)
            pattern = regex.find_date_Improved1(text[1])
            if (pattern is not None):
                result3.append(pattern)

        if len(result1) == 1:
            final_result = result1[0]
        if len(result1) == 0:
            b_set = set(result2)
            c_set = set(result3)
            final_result = c_set.intersection(b_set).pop()
        if len(result1) > 1:
            a_set = set(result1)
            b_set = set(result2)
            c_set = set(result3)
            final_result = c_set.intersection(a_set.intersection(b_set)).pop()
        print(final_result)
        print(str(final_result))
        counter = counter + 1
        file_str = str(filename) + ': ' + str(final_result)
        f = open('results.txt', 'a')
        f.write(file_str)
        f.write('\n')
        f.close()


