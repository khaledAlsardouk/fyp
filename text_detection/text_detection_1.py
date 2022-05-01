import easyocr
import os
import cv2
from matplotlib import pyplot as plt
import regex
import numpy as np


def OCR_TD(IMAGE_PATH):
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(IMAGE_PATH,decoder='greedy',batch_size=50)
        return result


#print(OCR_TD(r'./images/13.jpg'))