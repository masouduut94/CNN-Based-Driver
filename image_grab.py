import numpy as np
import pyscreenshot as ImageGrab
import cv2
import time



last_time = time.time()
while True:
    printscreenshot_pil = ImageGrab.grab(bbox=(0, 40, 640, 480))
    printscreenshot_numpy = np.array(printscreenshot_pil.getdata(), dtype='uint8')

    print('Loop took {} seconds'.format(time.time() - last_time))
    last_time = time.time()
    cv2.imshow('window', np.array(printscreenshot_pil))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break




