from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, Response, request

from background_subtraction.background_subtraction import BackgroundSubtractor
from base_constants.general_constants import FLASK_PORT
from cnn_architecture.cnn_architecture import CNNArchitecture
from frame_obtaining.frame_captor import FrameCaptor
from generator.frame_generator import frame_generator

app = Flask(__name__)
cnn_architecture = None



@app.route('/')
def entry_point():
    return render_template('index.html')


@app.route('/hra_stream')
def hra_stream():
    return render_template('recording_started.html')


@app.route('/stream_video', methods=['GET'])
def stream_video():
    # is_background_captured = request.form['is_background_captured']
    # is_background_captured = bool(is_background_captured)
    return Response(frame_generator(frame_captor, background_subtractor.is_background_captured()
                                    , cnn_architecture.predicted_letter),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    cnn_architecture = CNNArchitecture()
    frame_captor = FrameCaptor()
    frame_captor.set_capture_mode()
    background_subtractor = BackgroundSubtractor()
    http_server = WSGIServer(("127.0.0.1", FLASK_PORT), app)
    http_server.serve_forever()


