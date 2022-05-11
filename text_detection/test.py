import easyocr
import cv2
from matplotlib import pyplot as plt
import regex
import numpy as np
from ordered_set import OrderedSet

reader = easyocr.Reader(['en'])

IMAGE_PATH = r'C:\Users\tayeb\Desktop\New images\1.jpg'
result = reader.readtext(IMAGE_PATH,decoder='wordbeamsearch',batch_size=50)
print(result)

result1=[]
result2=[]
result3=[]

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
    result4 = ''
    b_set = OrderedSet(result2)
    c_set = OrderedSet(result3)
    print(c_set & b_set)
    for i in result2:
        for j in result3:
            y = b_set & c_set
    for i in y.copy():
        result4 = result4 + str(i)
        print(i)
        print(result4)
if  len(result1) > 1:
    a_set = OrderedSet(result1)
    b_set = OrderedSet(result2)
    c_set = OrderedSet(result3)
    print(c_set & (a_set & b_set))
print(result)
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