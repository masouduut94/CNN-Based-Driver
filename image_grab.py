import os, time, cv2
import numpy as np
from grab_screen import grab_screen
from getkeys import key_check

key_map = {
    'W': [1, 0, 0, 0, 0, 0, 0, 0, 0],
    'S': [0, 1, 0, 0, 0, 0, 0, 0, 0],
    'A': [0, 0, 1, 0, 0, 0, 0, 0, 0],
    'D': [0, 0, 0, 1, 0, 0, 0, 0, 0],
    'WS': [0, 0, 0, 0, 1, 0, 0, 0, 0],
    'WD': [0, 0, 0, 0, 0, 1, 0, 0, 0],
    'SA': [0, 0, 0, 0, 0, 0, 1, 0, 0],
    'SD': [0, 0, 0, 0, 0, 0, 0, 1, 0],
    'NK': [0, 0, 0, 0, 0, 0, 0, 0, 1],
    'default': [0, 0, 0, 0, 0, 0, 0, 0, 0],
}


def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    masked = cv2.rectangle(img=masked, pt1=(250, 250),
                           pt2=(550, 550), color=(0, 0, 0), thickness=-1)

    return masked


def keys_to_output(keys):
    if ''.join(keys) in key_map:
        return key_map[''.join(keys)]
    return key_map['default']


def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    vertices = np.array([[0, 270], [0, 100], [150, 20], [340, 20], [480, 130], [480, 270]], np.int32)
    processed_img = roi(processed_img, [vertices])
    return processed_img


while True:
    last_time = time.time()
    # key_catcher = MockButton()
    # Get raw pixels from the screen, save it to a Numpy array
    screen = grab_screen(region=(0, 40, 800, 640))
    # screen = cv2.resize(screen, (480, 270))
    # run a color convert:
    screen = cv2.resize(screen, (480, 270))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    keys = key_check()
    output = keys_to_output(keys)

    # Display the picture
    cv2.imshow("Window", screen)
    print('loop took {} seconds'.format(time.time() - last_time))
    k = cv2.waitKey(20)
    # Press "q" to quit

    if k & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
