from flask import render_template, session, request, Response
from facades.session_facade import SessionFacade


def get_base_template():
    session_facade = SessionFacade()
    session['session_facade'] = session_facade
    return render_template('index.html')


def get_streaming_template():
    session_facade = session.get('session_facade')
    session_facade.start_prediction()
    return Response(open('./templates/streaming.html').read(), mimetype="text/html")


def get_prediction():
    session_facade = session.get('session_facade')
    image_file = request.files['image']
    return session_facade.get_prediction_for_image(image_file)


# TODO: Add a way for the user to choose the hand from an UI settings page
# def set_used_hand():

