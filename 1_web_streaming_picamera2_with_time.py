from flask import Flask, render_template, Response
from picamera2 import Picamera2
import cv2 

import datetime
from PIL import ImageFont, ImageDraw, Image
import numpy as np 

app = Flask(__name__) 

#Picamera2 인스턴스 생성 및 카메라 설정 
picam2 = Picamera2() 
camera_config = picam2.create_still_configuration({"size":(640, 480)})
picam2.configure(camera_config) 
picam2.start()

# font : 시스템에 있는 기본 폰트 사용할 경우 
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)


def gen_frames(): 
    while True: 
        now = datetime.datetime.now() 
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        
        origin_frame = picam2.capture_array()
        frame = cv2.cvtColor(origin_frame, cv2.COLOR_RGB2BGR)
        
        frame = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame)
        
        # xy : 텍스트 시작 위기 
        #fill : 글자색 (Blue, GREEN, RED)
        draw.text(xy=(10, 15), text='HiRim Streaming '+nowDatetime, font=font, fill=(255, 255, 255))
        frame = np.array(frame)
         
        ret, buffer = cv2.imencode('.jpg', frame) 
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/') 
def index(): 
    return render_template('index.html') 

@app.route('/video_feed') 
def video_feed(): 
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__': 
    app.run(host='10.251.147.210', port='5000')
    #app.run(host='0.0.0.0', port='5000')
    
	
