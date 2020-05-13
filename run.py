from controllers.controller import Controller

if __name__ == '__main__':

    camera_init_url = "http://192.168.1.103:8080"
    controller = Controller(is_binary=False, camera_init_url=camera_init_url)
    controller.run_hand_prediction()
