from flask import Flask, render_template, Response
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = Flask(__name__)

f = open('C:/Users/ibrah/OneDrive/Skrivbord/programig/python/procjetct/qr scanner/myDataFile',)
myDataList = f.read().splitlines()


def generate_frames():
    cap = cv2.VideoCapture(0)  # 0 represents the default camera (you can change this to the desired source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width (adjust as needed)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height (adjust as needed)

    while True:
        success, frame = cap.read()
        for barcode in decode(frame):
            myData = barcode.data.decode('utf-8')
            print(myData)

            if myData in myDataList:
                myOutput = 'Authorized'
                myColor = (0, 255, 0)
            else:
                myOutput = 'Un-Authorized'
                myColor = (0, 0, 255)

            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, myColor, 5)
            pts2 = barcode.rect
            cv2.putText(frame, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            else:
                break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
