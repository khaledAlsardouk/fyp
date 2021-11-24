from PIL import Image
from pytesseract import pytesseract
import dateutil.parser as dparser
from datetime import datetime
import cv2

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = r"C:\Users\khale\Desktop\test\d.jpeg"

url = "http://192.168.1.105:8080/video"
cap = cv2.VideoCapture(url)
while(True):
    camera, frame = cap.read()
    if frame is not None:
        cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('y'):  # save on pressing
        cv2.imwrite('C:/Users/khale/Desktop/test/c1.png', frame)
        cv2.destroyAllWindows()
        break

img = Image.open('C:/Users/khale/Desktop/test/c1.png')
pytesseract.tesseract_cmd = path_to_tesseract
text = pytesseract.image_to_string(img)
print(text[:-1])
date = text[:-1]
date1 = date.split("EXP")
prod = dparser.parse(date1[0], fuzzy=True)
exp = dparser.parse(date1[1], fuzzy=True)
today = datetime.now()
x = (exp - today) / (today - prod)
low = 0.0209 * pow(x, 3) - 0.0948 * pow(x, 2) + 0.0899 * x + 0.0516
med = -0.00001 * pow(x, 5) + 0.00004 * pow(x, 4) - 0.0033 * pow(x, 3) - 0.0296 * pow(x, 2) + 0.3175 * x + 0.2856
high = -0.00001 * pow(x, 4) - 0.0002 * pow(x, 3) + 0.0179 * pow(x, 2) - 0.2414 * x + 1.8423
print(f'the production date is : {prod} \n the expiry date is : {exp}')
print(" low risk : " + str(low))
print(" med risk : " + str(med))
print(" high risk : " + str(high))
