import easyocr
import os
import cv2
from matplotlib import pyplot as plt
import regex
import re
import dateutil.parser as dparser
import numpy as np
from ordered_set import OrderedSet


reader = easyocr.Reader(['en'])

IMAGE_PATH = r'C:\Users\tayeb\Desktop\New folder\validation\384.jpg'
result = reader.readtext(IMAGE_PATH, decoder='wordbeamsearch', batch_size=50,width_ths=12)
result1 = []
result2 = []
result3 = []
final_result = ''

for text in result:
    pattern = regex.find_date_true(text[1])
    if pattern is not None:
        result1.append(pattern)
    pattern = regex.find_date_test_CMP1(text[1])
    if pattern is not None:
        result2.append(pattern)
    pattern = regex.find_date_Improved1(text[1])
    if pattern is not None:
        result3.append(pattern)
print(result1,result2,result3)
print(len(result1),len(result2),len(result3))
if len(result1) == 1:
    final_result = result1[0]
    print(result1)
elif len(result1) == 0:
    b_set = set(result2)
    c_set = set(result3)
    try:
        final_result = c_set.intersection(b_set).pop()
    except:
        final_result = 'no date found'
elif len(result1) > 1:
    a_set = OrderedSet(result1)
    b_set = OrderedSet(result2)
    c_set = OrderedSet(result3)
    print(a_set,b_set,c_set)
    try:
        final_result = c_set.intersection(b_set.intersection(a_set)).pop()
    except:
        final_result = 'no date found'
if len(result1) == 0 and len(result2) == 0:
    if result3:
        final_result = result3[0]
    else:
        final_result = 'no date found'
elif len(result1) == 0 and len(result3) == 0:
    if result2:
        final_result = result2[0]
    else:
        final_result = 'no date found'
print(final_result)
if (final_result) == 'no date found' and (len(result1) == 0 or len(result1) > 1):
    for text in result2:
        print(result2)
        for text1 in result3:
            print(result3)
            if (text in text1) or (text1 in text):
                if (len(text) > len(text1)):
                    final_result = text
                else:
                    final_result = text1
try:
    date = dparser.parse(final_result, fuzzy=True)
    print(str(date))
except:
    date = final_result
file_str =': date : ' + str(date) + " patterns result: " + str(final_result)
print(file_str)
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