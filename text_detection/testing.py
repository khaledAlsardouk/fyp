import easyocr
import os
import cv2
from matplotlib import pyplot as plt
import regex
import re
import dateutil.parser as dparser
import numpy as np


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


directory = r'C:\Users\tayeb\Desktop\New folder\training'
reader = easyocr.Reader(['en'])
dirlist = sorted_alphanumeric(os.listdir(directory))

for filename in dirlist:
    if filename.endswith(".jpg"):
        IMAGE_PATH = os.path.join(directory, filename)
        result = reader.readtext(IMAGE_PATH, decoder='wordbeamsearch', batch_size=50)
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
            try:
                final_result = c_set.intersection(b_set).pop()
            except:
                final_result = 'no date found'
        if len(result1) > 1:
            a_set = set(result1)
            b_set = set(result2)
            c_set = set(result3)
            try:
                final_result = c_set.intersection(b_set).pop()
            except:
                final_result = 'no date found'

        if len(result2) == 1:
            final_result = result2[0]

        if len(result2) == 0:
            b_set = set(result1)
            c_set = set(result3)
            try:
                final_result = c_set.intersection(b_set).pop()
            except:
                final_result = 'no date found'

        if len(result2) > 1:
            a_set = set(result1)
            b_set = set(result2)
            c_set = set(result3)
            try:
                final_result = c_set.intersection(b_set).pop()
            except:
                final_result = 'no date found'

        if len(result3) == 1:
            final_result = result3[0]

        if len(result3) == 0:
            b_set = set(result2)
            c_set = set(result1)
            try:
                final_result = c_set.intersection(b_set).pop()
            except:
                final_result = 'no date found'

        if len(result3) > 1:
            a_set = set(result1)
            b_set = set(result2)
            c_set = set(result3)
            try:
                final_result = c_set.intersection(b_set).pop()
            except:
                final_result = 'no date found'
        print(final_result)
        try:
            date = dparser.parse(final_result, fuzzy=True)
            print(str(date))
        except:
            date = final_result

        file_str = str(filename) + ': date : ' + str(date) + " patterns result: " + str(final_result)
        f = open('results2.txt', 'a')
        f.write(file_str)
        f.write('\n')
        f.close()
