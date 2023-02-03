# import the necessary packages``
import argparse
import base64
import datetime
import os
import shutil
import threading
import time
from threading import Event

import cv2
import numpy as np
from flask import Flask, Response, request
from flask_cors import CORS

outputFrame = np.zeros((480, 640, 3), dtype=np.uint8)
mode = 'static'
thread = None
lock = threading.Lock()
event = Event()

app = Flask(__name__)
CORS(app, origins=['*'])

camera_id = [0, 2, 4]
camera_pos = ['left', 'top', 'right']


@ app.route("/del_all")
def del_all():
    data_folder = 'data/'
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print("Error deleting file:", file_path)
                    print(e)
    return ("", 204)


@ app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    type = data.get("type").lower()
    variety = data.get("variety").lower()

    for filename in os.listdir("data/temp"):
        if os.path.isfile(os.path.join("data/temp", filename)):
            pos, ext = os.path.splitext(filename)
            copy(type, variety, pos)
    return ("", 204)


def copy(type, variety, pos):
    src_folder = "data/temp"
    dst_folder = f"data/{type}/{variety}/{pos}"
    src_filename = f"{pos}.jpg"
    count = [0]
    for file in os.listdir(dst_folder):
        if os.path.isfile(os.path.join(dst_folder, file)):
            root, ext = os.path.splitext(file)
            count.append(int(root))
    print(count)
    dst_filename = f"{max(count)+1}.jpg"
    src = src_folder + "/" + src_filename
    dst = dst_folder + "/" + dst_filename
    print(src)
    print(dst)
    shutil.copy(src, dst)
    os.unlink(src)


@ app.route("/reset", methods=["POST"])
def reset():
    try:
        event.set()
        thread.join()
    except:
        print("error")
    folder = "data/temp"
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    return ("", 204)


@ app.route("/image", methods=["POST"])
def image():
    data = request.get_json()
    imageId = data.get("imageId")
    response = Response(response=base64.b64encode(
        capture(imageId)).decode(), status=200, content_type='image/jpeg')
    return response


def capture(camera):
    try:
        event.set()
        thread.join()
    except:
        print("error")
    cap = None
    ret = None
    frame = None
    count = 0
    cap = cv2.VideoCapture(camera_id[camera])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

    while count < 40:
        ret, frame = cap.read()
        count = count + 1

    if ret:
        cap.release()
        cv2.imwrite(f"data/temp/{camera_pos[camera]}.jpg", frame)

        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (0, 255, 0)
        scale = 1
        thickness = 2
        text = camera_pos[camera]
        org = (50, 50)
        cv2.putText(frame, text, org, font,
                    scale, color, thickness, cv2.LINE_AA)

        success, encodedImage = cv2.imencode(".jpg", frame.copy())
        return encodedImage
    else:
        return None


@ app.route("/stream")  # /stream?camera=1&mode=static
def video():
    global mode
    camera = request.args.get('camera', default=1, type=int)
    mode = request.args.get('mode', default='static', type=str)
    return Response(generate(mode, camera),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def stream_vid(event, camera):
    global outputFrame, lock
    cap = cv2.VideoCapture(camera_id[camera])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    while True:
        if event.is_set():
            cap.release()
            break
        _, frame = cap.read()
        with lock:
            outputFrame = frame.copy()


def generate(mode, camera):
    global outputFrame, lock, thread
    if mode == 'stream':
        try:
            event.clear()
            thread = threading.Thread(target=stream_vid, args=(event, camera,))
            thread.daemon = True
            thread.start()
        except:
            print("error starting thread")
    elif mode == 'static':
        try:
            event.set()
            thread.join()
        except:
            print("error stopping thread")
        outputFrame = np.zeros((480, 640, 3), dtype=np.uint8)
    while True:
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


if __name__ == '__main__':
    del_all()
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, default="localhost",
                    help="ip address of the device")
    ap.add_argument("-p", "--port", type=int, default="5000",
                    help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())

    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=True)
