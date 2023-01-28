from flask import Flask
from flask_socketio import SocketIO
import cv2
import imutils
from collections import deque
from flask_cors import CORS

app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")
#socketio = SocketIO(app)

d = deque()

# Open the camera
cap = cv2.VideoCapture(2)

# Set the frame width and height
cap.set(3, 640)
cap.set(4, 480)


@socketio.on('connect')
def handle_connect():
    # Run in a loop indefinitely
    while True:
        # Read an image from the camera
        ret, frame = cap.read()

        if ret:
            # Resize the frame and encode it as JPEG
            frame = imutils.resize(frame, width=640)
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Send the frame over the WebSocket connection
            socketio.emit('frame', jpeg.tobytes())

            # Sleep for a short period of time to avoid overwhelming the WebSocket connection
            socketio.sleep(0.01)


if __name__ == '__main__':
    socketio.run(app)
