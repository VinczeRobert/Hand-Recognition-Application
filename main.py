from flask import Flask
from flask_session import Session
from gevent.pywsgi import WSGIServer
from base_constants.general_constants import FLASK_PORT
from controllers import controller

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST') # Put any other methods you need here
    return response


# @app.route('/video')
# def remote():
#     return Response(open('./templates/video.html').read(), mimetype="text/html")


if __name__ == '__main__':
    app.secret_key = 'any_random_string'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess = Session()
    sess.init_app(app)

    app.add_url_rule('/', view_func=controller.get_base_template, methods=['GET'])
    app.add_url_rule('/streaming', view_func=controller.get_streaming_template, methods=['GET'])
    app.add_url_rule('/prediction', view_func=controller.get_prediction, methods=['POST'])

    http_server = WSGIServer(("127.0.0.1", FLASK_PORT), app)
    http_server.serve_forever()

