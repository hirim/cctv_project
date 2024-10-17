from flask import Flask, render_template, Response, url_for, redirect
from picamera2 import Picamera2
import cv2
import datetime
from PIL import ImageFont, ImageDraw, Image
import numpy as np

app = Flask(__name__)

# Picamera2 인스턴스 생성 및 카메라 설정
picam2 = Picamera2()
camera_config = picam2.create_still_configuration({"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

is_capture = False

def gen_frames():
    global is_capture

    while True:
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        sanitized_datetime = now.strftime('%Y-%m-%d_%H-%M-%S')  # 파일명에 사용 가능한 형식

        origin_frame = picam2.capture_array()
        frame = cv2.cvtColor(origin_frame, cv2.COLOR_RGB2BGR)

        # 프레임에 텍스트 추가
        frame = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame)
        draw.text(xy=(10, 15), text='HiRim Streaming ' + nowDatetime, font=font, fill=(255, 255, 255))
        frame = np.array(frame)

        # 현재 프레임을 복사해서 캡처할 때 사용
        frame_for_capture = frame.copy()

        # 프레임을 JPEG로 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 캡처 버튼이 눌리면 이미지를 저장
        if is_capture:
            is_capture = False
            # 파일명에 현재 시간 포함, frame_for_capture로 이미지 저장
            cv2.imwrite(f'capture_{sanitized_datetime}.png', frame_for_capture)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/push_capture')
def push_capture():
    global is_capture
    is_capture = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='10.251.147.210', port='5000')
