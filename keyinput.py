from pynput.keyboard import Key, Controller

keyboard = Controller()

keys = {
    "w": 'w',
    "a": 'a',
    "s": 's',
    "d": 'd',
}

def press_key(key):
    keyboard.press(keys[key])

def release_key(key):
    keyboard.release(keys[key])
