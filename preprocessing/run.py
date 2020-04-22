from preprocessing.image_preprocessing import convert_folder_to_binary

if __name__ == '__main__':
    path = 'D:/Hand-Recognition-Application/data/daddy_photos'
    convert_folder_to_binary(path, True, 0.3)
