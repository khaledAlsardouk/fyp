from PIL import Image
from pytesseract import pytesseract
import dateutil.parser as dparser
import cv2
import numpy as np
# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = r"C:\Users\khale\Desktop\test\d.jpeg"

# url = "http://192.168.1.105:8080/video"
# cap = cv2.VideoCapture(url)
# while(True):
#     camera, frame = cap.read()
#     if frame is not None:
#         cv2.imshow("Frame", frame)
#     if cv2.waitKey(1) & 0xFF == ord('y'):  # save on pressing
#         cv2.imwrite('C:/Users/khale/Desktop/test/c1.png', frame)
#         cv2.destroyAllWindows()
#         break

img = Image.open('C:/Users/khale/Desktop/test/ko.jpeg')
pytesseract.tesseract_cmd = path_to_tesseract
text = pytesseract.image_to_string(img)
print(text[:-1])
# date=" pd:17/05/2000 exp:20/05/2000"
# date1=date.split("exp")
# date=dparser.parse(date1[0],fuzzy=True)
# date2=dparser.parse(date1[1],fuzzy=True)
# print(date1)
# print(date.month)
# print(date2)
#day , month ,year  = date.split("/")
#print("day:"+ str(day))



#img = Image.open(image_path)
#pytesseract.tesseract_cmd = path_to_tesseract
#text = pytesseract.image_to_string(img)

# Displaying the extracted text
#print(text[:-1])