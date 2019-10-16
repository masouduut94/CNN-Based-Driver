# Use of combination keys

from pynput.keyboard import Key, KeyCode, Listener

# Your functions


def up():
    print("Go up")


def down():
    print("Go down")


def left():
    print("Go left")


def right():
    print("Go right")


def up_left():
    print("Go up_left")


def up_right():
    print("Go up_right")


def down_left():
    print("Go down_left")


def down_right():
    print("Go down_right")


def do_nothing():
    print("Do Nothing")


# Create a mapping of keys to function (use frozenset as sets are not hashable - so they can't be used as keys)

combination_to_function = {
    frozenset([Key.up]): up,  # No `()` after function_1 because
    # we want to pass the function, not the value of the function
    frozenset([Key.down]): down,
    frozenset([Key.left]): left,
    frozenset([Key.right]): right,
    frozenset([Key.up, Key.left]): up_left,
    frozenset([Key.up, Key.right]): up_right,
    frozenset([Key.down, Key.left]): down_left,
    frozenset([Key.down, Key.right]): down_right,
}

# Currently pressed keys
current_keys = set()


def on_press(key):
    # When a key is pressed, add it to the set we are keeping track of and check if this set is in the dictionary
    current_keys.add(key)
    if frozenset(current_keys) in combination_to_function:
        # If the current set of keys are in the mapping, execute the function
        combination_to_function[frozenset(current_keys)]()


def on_release(key):
    # When a key is released, remove it from the set of keys we are keeping track of
    current_keys.remove(key)


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
