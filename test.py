import time

import cv2
import mss
import numpy as np


def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    return processed_img


with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 0, "left": 70, "width": 640, "height": 480}
    while True:
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        screen = np.array(sct.grab(monitor))
        new_screen = process_img(original_img=screen)

        # Display the picture
        cv2.imshow("Window", new_screen)

        print("Loop took {} seconds".format(time.time() - last_time))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
