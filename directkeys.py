"""from pykeyboard import PyKeyboard

"""
from pynput.keyboard import Key, Controller, Listener
import time
import ctypes

"""t1 = time.time()
keyboard = Controller()
keyboard.type('print("Hello python")')
print(time.time() - t1)
print("Hello python")"""

l = Listener()

