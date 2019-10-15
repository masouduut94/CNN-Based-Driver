from pynput.keyboard import Listener, Key

KEYS = {Key.up.name: 100, Key.down.name: 200, Key.left.name: 10,
        Key.right.name: 20, Key.esc.name: -20, Key.pause.name: -10}


class MockButton:

    def __init__(self):
        self.currently_pressed = set()
        self.is_pressed = False

        self.listener = Listener(on_press=self._on_press, on_release=self._on_release)
        self.start_listen()
        self.output = dict(
            up=self.up, down=self.down, left=self.left,
            right=self.right, up_left=self.up_left, up_right=self.up_right,
            down_left=self.down_left, down_right=self.down_right, pause=self.pause,
            quit=self.quit, default=self.default)

    def start_listen(self):
        self.listener.start()

    def _on_press(self, key):
        value = key.name if hasattr(key, 'name') else key.char
        try:
            if value in KEYS.keys():
                self.is_pressed = True
                self.currently_pressed.add(KEYS[key.name])
                print(self.currently_pressed)
                code = sum(self.currently_pressed)
                if code == 100:
                    self.output['up']()
                elif code == 200:
                    self.output['down']()
                elif code == 10:
                    self.output['left']()
                elif code == 20:
                    self.output['right']()
                elif code == -10:
                    self.output['pause']()
                elif code == -20:
                    self.output['quit']()
                elif code == 110:
                    self.output['up_left']()
                elif code == 120:
                    self.output['up_right']()
                elif code == 210:
                    self.output['down_left']()
                elif code == 220:
                    self.output['down_right']()
                else:
                    self.output['default']()
        except ValueError:
            pass

    def _on_release(self, key):
        try:
            self.currently_pressed.remove(key.value)

            if self.is_pressed and len(self.currently_pressed) == 0:
                self.is_pressed = False

        except KeyError:
            pass

    def stop_listen(self):
        self.listener.stop()

    def up(self):
        print("Go Up!")

    def down(self):
        print("Go Down!")

    def left(self):
        print("Go left!")

    def right(self):
        print("Go right!")

    def up_left(self):
        print("Go up_left!")

    def up_right(self):
        print("Go up_right!")

    def down_right(self):
        print("Go down_right!")

    def down_left(self):
        print("Go down_left!")

    def quit(self):
        print("Over")

    def pause(self):
        print("Paused!")

    def default(self):
        print("Do Nothing!")






