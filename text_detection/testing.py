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


directory = r'C:\Users\tayeb\Desktop\New images'
reader = easyocr.Reader(['en','la'])
dirlist = sorted_alphanumeric(os.listdir(directory))

for filename in dirlist:
    if filename.endswith(".jpg"):
        IMAGE_PATH = os.path.join(directory, filename)
        result = reader.readtext(IMAGE_PATH, decoder='wordbeamsearch', batch_size=50)
        result1 = []
        result2 = []
        result3 = []
        final_result = ''
        print(result)
        for text in result:
            pattern = regex.find_date_true(text[1])
            if (pattern is not None):
                result1.append(pattern)
                print(pattern)
            pattern = regex.find_date_test_CMP1(text[1])
            if (pattern is not None):
                result2.append(pattern)
                print(pattern)
            pattern = regex.find_date_Improved1(text[1])
            if (pattern is not None):
                result3.append(pattern)
                print(pattern)
        if len(result1) == 1:
            final_result = result1[0]
        elif len(result1) == 0:
            b_set = set(result2)
            c_set = set(result3)
            if (c_set is not None) and (b_set is not None):
                try:
                    final_result = c_set.intersection(b_set).pop()
                except:
                    final_result = 'no date found'
            elif b_set is not None:
                final_result = b_set
            elif c_set is not None:
                final_result = c_set
        elif len(result1) > 1:
            a_set = set(result1)
            b_set = set(result2)
            c_set = set(result3)
            if (c_set is not None) and (b_set is not None) and (a_set is not None):
                try:
                    final_result = c_set.intersection(b_set.intersection(a_set)).pop()
                except:
                    final_result = 'no date found'
            elif len(a_set) == 0:
                try:
                    final_result = c_set.intersection(b_set).pop()
                except:
                    final_result = 'no date found'
            elif len(b_set) == 0:
                try:
                    final_result = c_set.intersection(a_set).pop()
                except:
                    final_result = 'no date found'
            elif len(c_set) == 0:
                try:
                    final_result = a_set.intersection(b_set).pop()
                except:
                    final_result = 'no date found'
            elif len(a_set) == 0 and len(b_set) == 0:
                final_result = c_set
            elif len(a_set) == 0 and len(c_set) == 0:
                final_result = b_set
            elif len(b_set) == 0 and len(c_set) == 0:
                final_result = a_set
        try:
            date = dparser.parse(final_result, fuzzy=True)
            print(str(date))
        except:
            date = final_result

        file_str = str(filename) + ': date : ' + str(date) + " patterns result: " + str(final_result)
        f = open('new_results.txt', 'a')
        f.write(file_str)
        f.write('\n')
        f.close()

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
