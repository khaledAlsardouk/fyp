import easyocr
import os
import cv2
from matplotlib import pyplot as plt
import regex
import re
import dateutil.parser as dparser
import numpy as np
from pyzbar.pyzbar import decode


def OCR_TD(IMAGE_PATH):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(IMAGE_PATH, decoder='wordbeamsearch', batch_size=50, width_ths=12)
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

    if len(result1) == 1:
        final_result = result1[0]
    elif len(result1) == 0:
        b_set = set(result2)
        c_set = set(result3)
        try:
            final_result = c_set.intersection(b_set).pop()
        except:
            final_result = 'no date found'
    elif len(result1) > 1:
        a_set = set(result1)
        b_set = set(result2)
        c_set = set(result3)
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
    if (final_result) == 'no date found' and (len(result1) == 0 or len(result1) > 1):
        for text in result2:
            for text1 in result3:
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
    return str(date)



def extract_barcode(IMAGE_PATH):
    img = cv2.imread(IMAGE_PATH)

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
                print(str(barcode.data))
                return (str(barcode.data))
