import easyocr
import os
import cv2
from matplotlib import pyplot as plt
import regex
import numpy as np
directory = 'C:/Users/tayeb/Desktop/New folder/training'
counter = 0
reader = easyocr.Reader(['en'])
for filename in os.listdir(directory):
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
                print(pattern)
        for text in result:
            pattern = regex.find_date_test_CMP1(text[1])
            if (pattern is not None):
                result2.append(pattern)
                print(pattern)
        for text in result:
            pattern = regex.find_date_Improved1(text[1])
            if (pattern is not None):
                result3.append(pattern)
                print(pattern)
        print(result1)
        print(result2)
        print(result3)
        if len(result1) == 0:
            b_set = set(result2)
            c_set = set(result3)
            final_result = c_set.intersection(b_set)
            print(c_set.intersection(b_set))
        if len(result1) > 1:
            a_set = set(result1)
            b_set = set(result2)
            c_set = set(result3)
            final_result = c_set.intersection(a_set.intersection(b_set))
            print(c_set.intersection(a_set.intersection(b_set)))
        for text in result:
            pattern = regex.find_date_improved(text[1])
            if (pattern is not None):
                print(pattern)
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
        print(result)
        for text in result:
            pattern = regex.find_parser(text[1])
            if (pattern is not None):
                print(text[1])
                print(pattern)
        counter = counter + 1
        file_str = str(counter) + ': ' + str(final_result)
        f = open('results.txt', 'a')
        f.write(file_str)
        f.write('\n')
        f.close()


