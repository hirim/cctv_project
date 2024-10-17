from flask import Flask, render_template, Response, url_for, redirect
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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

global push_btn 
push_btn = False

def gen_frames(): 
    while True: 
        now = datetime.datetime.now() 
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        
        origin_frame = picam2.capture_array()
        frame = cv2.cvtColor(origin_frame, cv2.COLOR_RGB2BGR)
        
        if push_btn : 
            frame = np.zeros([480, 640, 3], dtype='uint8') # openCV 가로 세로 바뀜 RGB 형식 검은 화면 생성 
            frame = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame)
            
            draw.text(xy=(10, 15), text='HiRim Streaming '+ nowDatetime, font=font, fill=(255, 255,255))
            draw.text(xy=(320,  240), text='Streaming OFF', font=font, fill=(255, 255, 255))  
            frame = np.array(frame)
        else : 
            frame = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame)
            
            draw.text(xy=(10, 15), text='HiRim Streaming '+ nowDatetime, font=font, fill=(255, 255,255))
            frame = np.array(frame)
         
        ret, buffer = cv2.imencode('.jpg', frame) 
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/') 
def index(): 
    global push_btn
    return render_template('index2.html', push_btn = push_btn) 

@app.route('/video_feed') 
def video_feed(): 
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/push_switch')
def push_switch():
    global push_btn
    push_btn = not push_btn
    return redirect(url_for('index'))


if __name__ == '__main__': 
    app.run(host='10.251.147.210', port='5000')

    
	
