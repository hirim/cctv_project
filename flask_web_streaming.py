from flask import Flask, render_template, Response
from picamera2 import Picamera2
import cv2 

app = Flask(__name__) 

#Picamera2 인스턴스 생성 및 카메라 설정 
picam2 = Picamera2() 
camera_config = picam2.create_still_configuration({"size":(640, 480)})
picam2.configure(camera_config) 
picam2.start() 

def gen_frames(): 
    while True: 
        frame = picam2.capture_array()
        ref, buffer = cv2.imencode('.jpg', frame) 
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/') 
def index(): 
    return render_template('index.html') 

@app.route('/video_feed') 
def video_feed(): 
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__': 
    #app.run(host='10.251.147.210', port='5000')
    app.run(host='0.0.0.0', port='5000')
    
	
