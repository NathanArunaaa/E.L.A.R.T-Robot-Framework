from flask import Flask, render_template, request, Response
import cv2

app = Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0)  # Use 0 for the default webcam, or specify the device ID if multiple webcams are connected
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Convert the frame to a byte array
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control_robot():
    command = request.form['command']
    
    return 'Command received: ' + command


@app.route('/shutdown', methods=['POST'])
def shutdown():
    quit()
    return 'Application shutting down...'

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
