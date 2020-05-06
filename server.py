from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, Response, request
from background_subtraction.background_subtraction import BackgroundSubtractor
from base_constants.general_constants import FLASK_PORT, WEIGHTS_RIGHT_PATH, WEIGHTS_LEFT_PATH
from cnn_architecture.cnn_architecture import CNNArchitecture
from frame_obtaining.frame_captor import FrameCaptor
from generator.frame_generator import simple_frame_generator, predicted_frame_generator

app = Flask(__name__)
cnn_architecture = None


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/streaming', methods=['GET'])
def streaming():
    return render_template('recording_started.html')


@app.route('/stream_simple', methods=['GET'])
def stream_simple():
   return Response(simple_frame_generator(frame_captor),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/stream_with_predictions', methods=['GET'])
def stream_with_predictions():
    return Response(predicted_frame_generator(frame_captor, background_subtractor, cnn_architecture),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    cnn_architecture = CNNArchitecture()
    cnn_architecture.build_model()
    cnn_architecture.model.load_weights(WEIGHTS_LEFT_PATH)
    frame_captor = FrameCaptor(hand_index=1)
    frame_captor.set_capture_mode()
    background_subtractor = BackgroundSubtractor()
    http_server = WSGIServer(("127.0.0.1", FLASK_PORT), app)
    http_server.serve_forever()


