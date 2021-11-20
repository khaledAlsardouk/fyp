from PIL import Image
from pytesseract import pytesseract
import cv2
import numpy as np
# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = r"C:\Users\khale\Desktop\test\d.jpeg"

url = "http://192.168.1.107:8080/video"
cap = cv2.VideoCapture(url)
while(True):
    camera, frame = cap.read()
    if frame is not None:
        cv2.imshow("Frame", frame)
    q = cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('y'):  # save on pressing 'y'
        cv2.imwrite('C:/Users/khale/Desktop/test/c1.png', frame)
        cv2.destroyAllWindows()
        break

img = Image.open('C:/Users/khale/Desktop/test/c1.png')
pytesseract.tesseract_cmd = path_to_tesseract
text = pytesseract.image_to_string(img)
print(text[:-1])

print("no text")

#img = Image.open(image_path)
#pytesseract.tesseract_cmd = path_to_tesseract
#text = pytesseract.image_to_string(img)

# Displaying the extracted text
#print(text[:-1])