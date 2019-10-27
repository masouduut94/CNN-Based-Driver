import cv2, time, random
import numpy as np
from grab_screen import grab_screen
from getkeys import key_check
from collections import deque
from models import inception_v3 as google_net
from pynput.keyboard import Controller
from statistics import mean
from motion import motion_detection

GAME_WIDTH = 800
GAME_HEIGHT = 600

log_len = 25
motion_req = 800
motion_log = deque(maxlen=log_len)

WIDTH = 480
HEIGHT = 270
LR = 1e-3
EPOCHS = 10

keyboard = Controller()


def straight():
    keyboard.press('w')
    keyboard.release('a')
    keyboard.release('d')
    keyboard.release('s')


def left():
    if random.randrange(0, 3) == 1:
        keyboard.press('w')
    else:
        keyboard.release('w')
    keyboard.press('a')
    keyboard.release('s')
    keyboard.release('d')


def right():
    if random.randrange(0, 3) == 1:
        keyboard.press('w')
    else:
        keyboard.release('w')
    keyboard.press('d')
    keyboard.release('s')
    keyboard.release('d')


def reverse():
    keyboard.press('s')
    keyboard.release('a')
    keyboard.release('w')
    keyboard.release('d')


def forward_left():
    keyboard.press('w')
    keyboard.press('a')
    keyboard.release('s')
    keyboard.release('d')


def forward_right():
    keyboard.press('w')
    keyboard.press('d')
    keyboard.release('s')
    keyboard.release('a')


def reverse_left():
    keyboard.press('s')
    keyboard.press('a')
    keyboard.release('w')
    keyboard.release('d')


def reverse_right():
    keyboard.press('s')
    keyboard.press('d')
    keyboard.release('w')
    keyboard.release('a')


def no_keys():
    if random.randrange(0, 3) == 1:
        keyboard.press('w')
    else:
        keyboard.release('w')

    keyboard.release('a')
    keyboard.release('s')
    keyboard.release('d')


model = google_net(WIDTH, HEIGHT, 3, LR, output=9)
MODEL_NAME = './model_1.model'
model.load(MODEL_NAME)

print('We have loaded a previous model!!!')

actions = {0: straight, 1: reverse, 2: left, 3: right, 4: forward_left, 5: forward_right, 6: reverse_left,
           7: reverse_right, 8: no_keys}

mode_name = {0: 'straight', 1: 'reverse', 2: 'left', 3: 'right', 4: 'forward_left', 5: 'forward_right',
             6: 'reverse_left', 7: 'reverse_right', 8: 'no_keys'}


def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)
    paused = False
    mode_choice = 0

    screen = grab_screen(region=(0, 40, GAME_WIDTH, GAME_HEIGHT + 40))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    prev = cv2.resize(screen, (WIDTH, HEIGHT))

    t_minus, t_now, t_plus = prev, prev, prev

    while True:
        if not paused:
            screen = grab_screen(region=(0, 40, GAME_WIDTH, GAME_HEIGHT + 40))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            last_time = time.time()
            screen = cv2.resize(screen, (WIDTH, HEIGHT))

            delta_count_last = motion_detection(t_minus, t_now, t_plus)

            t_minus = t_now
            t_now = t_plus
            t_plus = screen
            t_plus = cv2.blur(t_plus, (4, 4))

            prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 3)])[0]
            prediction = np.array(prediction) * np.array([4.5, 0.1, 0.1, 0.1, 1.8, 1.8, 0.5, 0.5, 0.2])

            mode_choice = int(np.argmax(prediction))
            actions[mode_choice]()
            choice_picked = mode_name[mode_choice]

            motion_log.append(delta_count_last)
            motion_avg = round(mean(motion_log), 3)
            print(
                'loop took {0} seconds. Motion: {1}. Choice: {2}'.format(round(time.time() - last_time, 3), motion_avg,
                                                                         choice_picked))

            if motion_avg < motion_req and len(motion_log) >= log_len:
                print('WERE PROBABLY STUCK FFS, initiating some evasive maneuvers.')

                # 0 = reverse straight, turn left out
                # 1 = reverse straight, turn right out
                # 2 = reverse left, turn right out
                # 3 = reverse right, turn left out

                quick_choice = random.randrange(0, 4)
                if quick_choice == 0:
                    reverse()
                    time.sleep(random.uniform(1, 2))
                    forward_left()
                    time.sleep(random.uniform(1, 2))

                elif quick_choice == 1:
                    reverse()
                    time.sleep(random.uniform(1, 2))
                    forward_right()
                    time.sleep(random.uniform(1, 2))

                elif quick_choice == 2:
                    reverse_left()
                    time.sleep(random.uniform(1, 2))
                    forward_right()
                    time.sleep(random.uniform(1, 2))

                elif quick_choice == 3:
                    reverse_right()
                    time.sleep(random.uniform(1, 2))
                    forward_left()
                    time.sleep(random.uniform(1, 2))

                for i in range(log_len - 2):
                    del motion_log[0]

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                keyboard.release('a')
                keyboard.release('w')
                keyboard.release('d')
                time.sleep(1)


if __name__ == "__main__":
    main()




