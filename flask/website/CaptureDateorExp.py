from flask import Flask, render_template, Response, request, flash,Blueprint
import cv2
import datetime, time
from flask_sqlalchemy import SQLAlchemy
from.models import Item
import text_detection_1 as td
import asyncio
from os import path

global capture, switch, frame, BarOrExp
Capture1=Blueprint("Capture1",__name__)



DB_NAME = "Items.db"
date = "HI"
heading = ("Item name", "Expiry", "notfication date", "Category")
capture = 0  # to capture image
switch = 0  # to turn the camera on and off
barcode = 0  # indicates barcode's turn
app = Flask(__name__)
app.secret_key = "secret key"
# url = 'http://192.168.1.103:8080/video'
url = 1
data = []


def getItemFromDb(itemID):
    global date
    items = Item.query.filter_by(Barcode=itemID).first()
    print(items)
    data.append([items.Item_name, date, items.Category])


def popups1():
    global BarOrExp, barcode
    if barcode == 1:
        BarOrExp = "Please Scan The Barcode"
    else:
        BarOrExp = "Please Scan Expiry Date"
    return BarOrExp


def capture_exp_images():
    global frame, capture, switch, barcode, heading, date
    capture = 0
    now = (datetime.datetime.now()).strftime("%f")  # generate name based on time
    image_path = './shots/exp' + now + '.jpg'  # name for exp image
    switch = 0  # turn off switch
    camera.release()  # turn off camera
    cv2.imwrite(image_path, frame)  # save barcode image            #exp479403.jpg
    barcode = 1
    date = td.OCR_TD(image_path)


def capture_bar_images():
    global frame, capture, switch, barcode
    capture = 0
    now = (datetime.datetime.now()).strftime("%f")  # generate name based on time
    image_path = './shots/bar' + now + '.jpg'  # name for barcode image
    switch = 0  # turn off switch
    camera.release()  # turn off camera
    cv2.imwrite(image_path, frame)  # save barcode image
    barcode = 0  # reset barcode turn
    extracted_Num = td.extract_barcode(image_path)
    getItemFromDb(extracted_Num)


@Capture1.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames():  # camera
    global frame, capture, switch, barcode
    while switch:

        ## read the camera frame
        success, frame = camera.read()
        if success:
            if (capture == 1 and barcode == 0):
                capture_exp_images()
            if (capture == 1 and barcode == 1):
                capture_bar_images()
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            break


@Capture1.route("/Capture", methods=['GET', 'POST'])
def Capture():
    global switch, camera
   
    if request.method == 'POST':
        if request.form.get('stop') == 'Stop/Start':
            if switch == 0:
                switch = 1
                camera = cv2.VideoCapture(url)
            else:
                switch = 0
                camera.release()
        elif request.form.get('click') == 'Capture':  # capture current frame
            global capture
            # flash('here1')
            capture = 1
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('ExpOrBar.html', flash_message="False")
    return render_template('ExpOrBar.html', flash_message="True", Message=popups1(), headings=heading, Date=date,datas=data)


