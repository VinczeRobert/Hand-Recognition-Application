import cv2 as cv
from preprocessing.image_preprocessing import scaling_with_padding

if __name__ == '__main__':
    path = 'C:/Users/robi997/Downloads/Hand_Gesture_Dataset/Training/Only_Letters_Binary/G/hand1_g_bot_seg_2_cropped.png'
    image = cv.imread(path, cv.IMREAD_UNCHANGED)
    cv.imshow("Original", image)
    # rotated = rotating(image, 30, True)
    # finding_bounding_box(rotated, True)
    scaling_with_padding(image, 1.2, True)
    cv.waitKey(0)