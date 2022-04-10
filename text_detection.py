import easyocr
import cv2
from matplotlib import pyplot as plt
import regex
import numpy as np

IMAGE_PATH = r"C:\Users\khale\Desktop\fyp\test-STUFF\dataset-dates\training\2.jpg"
reader = easyocr.Reader(['en'])
result = reader.readtext(IMAGE_PATH)
top_left = tuple(result[0][0][0])
bottom_right = tuple(result[0][0][2])
text = result[0][1]
img = cv2.imread(IMAGE_PATH)
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
plt.figure(figsize=(10, 10))
plt.imshow(img)
plt.show()


