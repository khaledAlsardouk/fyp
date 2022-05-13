from flask import Flask, render_template, Response,request, flash
import cv2
import datetime, time
import os
#import text_detection_1 as td
global capture, switch, frame, BarOrExp
import sys


capture=0       #to capture image
switch=0        #to turn the camera on and off
barcode = 0     #indicates barcode's turn
app = Flask(__name__)
app.secret_key = "secret key"
url = 'http://192.168.2.237:8080/video'
camera = cv2.VideoCapture(0)    #cahnge 0 to url for IP web

def popups1():
    global BarOrExp, barcode
    if(barcode==1):
        BarOrExp = "Please Scan The Barcode"
    else:
        BarOrExp = "Please Scan Expiry Date"
    return BarOrExp


def capture_exp_images():
    global frame, capture, switch, barcode
    capture = 0
    now = (datetime.datetime.now()).strftime("%f")  # generate name based on time
    image_path = './shots/exp' + now + '.jpg'  # name for exp image
    switch = 0  # turn off switch
    camera.release()  # turn off camera
    cv2.imwrite(image_path, frame)  # save barcode image
    barcode = 1

def capture_bar_images():
    global frame, capture, switch, barcode
    capture = 0
    now = (datetime.datetime.now()).strftime("%f")  # generate name based on time
    image_path = './shots/bar' + now + '.jpg'  # name for barcode image
    switch = 0  # turn off switch
    camera.release()  # turn off camera
    cv2.imwrite(image_path, frame)  # save barcode image
    barcode = 0  # reset barcode turn


def generate_frames():      #camera
    global frame, capture, switch,barcode
    while switch:

        ## read the camera frame
        success, frame = camera.read()
        if success:
            if (capture == 1 and barcode==0):
                capture_exp_images()
                # capture = 0
                # now = (datetime.datetime.now()).strftime("%f")  # generate name based on time
                # image_path = './shots/exp' + now + '.jpg'       #name for exp image
                # switch = 0                                      #turn off switch
                # camera.release()                                #turn off camera
                # cv2.imwrite(image_path, frame)                  #save barcode image
                # barcode = 1                                     #set barcode turn
                #flash(str(image_path))           #shows the path
                #print(image_path, file=sys.stderr)
                #flask.jsonify("help") #REUTRN EXP HERE HELPP HEREEEEEEEEEEEEEEEEEEEP
            if (capture == 1 and barcode == 1):
                capture_bar_images()
                # capture = 0
                # now = (datetime.datetime.now()).strftime("%f")  # generate name based on time
                # image_path = './shots/bar' + now + '.jpg'       #name for barcode image
                # switch = 0                                      #turn off switch
                # camera.release()                                #turn off camera
                # cv2.imwrite(image_path, frame)                  #save barcode image
                # barcode = 0                                     #reset barcode turn
                #flash(str(image_path))                  #shows the path
                #print(image_path, file=sys.stderr)
                #flask.jsonify("help") #Implement BARCODE LATERRRRRRRRRRRRRRRRRRRRRR

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            break






@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/", methods=['GET', 'POST'])
def index():
    global switch, camera
    #success, frame = camera.read()
    if request.method == 'POST':
        if request.form.get('stop') == 'Stop/Start':
            if(switch==0):
                switch = 1
                camera = cv2.VideoCapture(0)
            else:
                switch=0
                camera.release()
        elif request.form.get('click') == 'Capture':        #capture current frame
            global capture
            #flash('here1')
            capture = 1
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('capture.html', barorexp = popups1())

    return render_template("capture.html", barorexp = popups1())

@app.route('/')
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


if __name__ == "__main__":
    app.run(debug=True)