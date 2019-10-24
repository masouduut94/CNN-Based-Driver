import os
import numpy as np
from cv2 import cvtColor, resize, COLOR_BGR2RGB
from time import sleep, time
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

starting_value = 1

while True:
    file_name = 'training_data-{0}.npy'.format(starting_value)
    if os.path.isfile(file_name):
        print('File exists, moving along', starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!', starting_value)
        break


def keys_to_output(keys):
    if ''.join(keys) in key_map:
        return key_map[''.join(keys)]
    return key_map['default']


def main(file_name, starting_value):
    training_data = []
    for i in list(range(4))[::-1]:
        print(i + 1)
        sleep(1)

    # last_time = time()
    paused = False
    print('STARTING!!!')
    while True:
        if not paused:
            screen = grab_screen(region=(30, 30, 800, 600))
            last_time = time()
            # resize to something a bit more acceptable for a CNN
            screen = resize(screen, (480, 270))
            # run a color convert:
            screen = cvtColor(screen, COLOR_BGR2RGB)
            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen, output])

            if len(training_data) % 100 == 0:
                print(len(training_data))
                if len(training_data) == 500:
                    np.save(file_name, training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = 'C:/Users/masoud/Desktop/PycharmProjects/CNN-Based-Driver/data/training_data-{0}.npy'.\
                        format(starting_value)

        keys = key_check()
        if 'P' in keys:
            if paused:
                paused = False
                print('Unpaused!')
                sleep(1)
            else:
                print('Pausing!')
                paused = True
                sleep(1)
        if 'I' in keys:
            break


if __name__ == "__main__":
    main(file_name, starting_value)
