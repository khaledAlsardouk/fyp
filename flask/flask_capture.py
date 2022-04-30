from flask import Flask, render_template, Response,request, flash
import cv2
import datetime, time
import os
import text_detection_1 as td
global capture, switch, frame


capture=0       #to capture image
switch=0        #to turn the camera on and off
app = Flask(__name__)
app.secret_key = "secret key"
url = 'http://192.168.2.237:8080/video'
camera = cv2.VideoCapture(0)    #cahnge 0 to url for IP web
SAVED_FOLDER = 'shots/'        #directory for saved images

def generate_frames():      #camera
    global frame
    while switch:

        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'           
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/", methods=['GET', 'POST'])
def index():
    global switch, capture
    success, frame = camera.read()
    if request.method == 'POST':
        if request.form.get('stop') == 'Stop/Start':
            if(switch==0):
                switch = 1
            else: switch = 0
        elif request.form.get('click') == 'Capture':        #caotuer current frame
            capture = 0
            switch = 0
            now = (datetime.datetime.now()).strftime("%f")  #generate name based on time
            image_path = os.path.sep.join(['shots', "shot_{}.jpg".format(str(now).replace(":", ''))])
            cv2.imwrite(image_path, frame)
            #image_path= image_path.replace("\\","/")
            #flash(image_path)       shows the
            #flash(td.OCR_TD(image_path))
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)