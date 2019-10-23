from pynput.keyboard import Key, Listener
# Currently pressed keys
current_keys = set()


class KeyToOutput:
    def __init__(self):
        # Create a mapping of keys to function (use frozenset as sets are not hashable - so they can't be used as keys)
        self.keys_to_function = {
            frozenset([Key.up]): self.up,
            frozenset([Key.down, ]): self.down,
            frozenset([Key.left, ]): self.left,
            frozenset([Key.right, ]): self.right,
            frozenset([Key.up, Key.left]): self.up_left,
            frozenset([Key.up, Key.right]): self.up_right,
            frozenset([Key.down, Key.left]): self.down_left,
            frozenset([Key.down, Key.right]): self.down_right,
        }
        self.vectors = {
            'up':         [1, 0, 0, 0, 0, 0, 0, 0, 0],
            'down':       [0, 1, 0, 0, 0, 0, 0, 0, 0],
            'left':       [0, 0, 1, 0, 0, 0, 0, 0, 0],
            'right':      [0, 0, 0, 1, 0, 0, 0, 0, 0],
            'up_right':   [0, 0, 0, 0, 1, 0, 0, 0, 0],
            'up_left':    [0, 0, 0, 0, 0, 1, 0, 0, 0],
            'down_left':  [0, 0, 0, 0, 0, 0, 1, 0, 0],
            'down_right': [0, 0, 0, 0, 0, 0, 0, 1, 0],
            'do_nothing': [0, 0, 0, 0, 0, 0, 0, 0, 1]
        }

        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def up(self):
        return self.vectors['up']

    def down(self):
        return self.vectors['down']

    def left(self):
        return self.vectors['left']

    def right(self):
        return self.vectors['right']

    def up_left(self):
        return self.vectors['up_left']

    def up_right(self):
        return self.vectors['up_right']

    def down_left(self):
        return self.vectors['down_left']

    def down_right(self):
        return self.vectors['down_right']

    def do_nothing(self):
        return self.vectors['do_nothing']

    def on_press(self, key):
        # When a key is pressed, add it to the set we are keeping track of and check if this set is in the dictionary
        current_keys.add(key)
        if frozenset(current_keys) in self.keys_to_function:
            # If the current set of keys are in the mapping, execute the function
            self.keys_to_function[frozenset(current_keys)]()

    @staticmethod
    def on_release(key):
        # When a key is released, remove it from the set of keys we are keeping track of
        if key in current_keys:
            current_keys.remove(key)
