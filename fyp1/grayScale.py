from PIL import Image
from pytesseract import pytesseract
import dateutil.parser as dparser
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
import ctypes


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


Mbox('expiry', 'scan the expiry date', 1)

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
url = "http://192.168.1.100:8080/video"


def calculate_eq(prod, exp, today, risk):
    x = (exp - today) / (today - prod)
    print(f'the production date is : {prod} \n the expiry date is : {exp}')
    if 'low' in risk:
        low = 0.0209 * pow(x, 3) - 0.0948 * pow(x, 2) + 0.0899 * x + 0.0516
        print(" low risk : " + str(low))
        return
    elif 'med' in risk:
        med = -0.00001 * pow(x, 5) + 0.00004 * pow(x, 4) - 0.0033 * pow(x, 3) - 0.0296 * pow(x, 2) + 0.3175 * x + 0.2856
        print(" med risk : " + str(med))
        return
    elif 'high' in risk:
        high = -0.00001 * pow(x, 4) - 0.0002 * pow(x, 3) + 0.0179 * pow(x, 2) - 0.2414 * x + 1.8423
        print(" high risk : " + str(high))
        return


def capture_image(url):
    cap = cv2.VideoCapture(url)
    while (True):
        camera, frame = cap.read()
        if frame is not None:
            cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('y'):  # save on pressing
            cv2.imwrite('c1.png', frame)
            cv2.destroyAllWindows()
            break


def extract_dates():
    img = Image.open('c2.png')
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(img)
    print(text[:-1])
    date = text[:-1]
    date1 = date.split("EXP")
    prod = dparser.parse(date1[0], fuzzy=True)
    exp = dparser.parse(date1[1], fuzzy=True)
    today = datetime(2021, 11, 21)
    return prod, today, exp


def extract_barcode():
    img = cv2.imread("c1.png")

    # Decode the barcode image
    detectedBarcodes = decode(img)

    # If not detected then print the message
    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:

        # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes:

            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect

            # Put the rectangle in image using
            # cv2 to heighlight the barcode
            cv2.rectangle(img, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (255, 0, 0), 2)

            if barcode.data != "":
                # Print the barcode data
                print(barcode.data)
                return str(barcode.data)


def searchitems(input):
    obj1 = open("items.txt")

    for line in obj1.readlines():
        line = line.rstrip()
        if input in line:
            line=line.split(" ")
            print("item type : " +line[1])
            print("risk: " + line[2])
            obj1.close()
            return line


capture_image(url)
prod, today, exp = extract_dates()
Mbox('barcode', 'scan the barcode', 1)
capture_image(url)
barcode_Num = extract_barcode()
type = searchitems(barcode_Num)
calculate_eq(prod, exp, today, type[2])
