def frame_generator(frame_obtainer, is_background_captured, predicted_letter):
    while True:
        frame = frame_obtainer.read_frame(is_background_captured, predicted_letter)
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
