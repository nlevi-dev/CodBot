import keyboard
from PIL import ImageGrab
import time
import numpy as np
from util import test_profile, take_screenshot
import pydirectinput
import random

global running
running = True

state_names = ['ingame','endgame','confirm','pregame','none']
profiles = [np.load('profiles/'+name+'.npy') for name in state_names[:-1]]

def get_state():
    screenshot = np.flip(np.array(ImageGrab.grab()),2)
    for i in range(len(profiles)):
        if test_profile(profiles[i], screenshot):
            return i
    return len(profiles)

def toggle():
    global running
    running = not running
    if running:
        print('Running!')
    else:
        print('Stopped!')

keyboard.add_hotkey('ctrl+t', toggle)
keyboard.add_hotkey('ctrl+l', take_screenshot)

previous = ''
state = ''
stamp = time.time()
while True:
    time.sleep(0.1 if state == 'ingame' else 1)
    if running:
        state = state_names[get_state()]
        if state != previous:
            stamp = time.time()
        if state == 'ingame':
            pydirectinput.keyDown('w')
            for _ in range(3):
                if random.random() < 0.3:
                    pydirectinput.keyDown('a')
                    time.sleep(1)
                    pydirectinput.keyUp('a')
                elif random.random() < 0.3:
                    pydirectinput.keyDown('d')
                    time.sleep(1)
                    pydirectinput.keyUp('d')
                else:
                    time.sleep(1)
                if random.random() < 0.2:
                    pydirectinput.click()
                time.sleep(1)
            pydirectinput.keyUp('w')
        elif state == 'endgame':
            pydirectinput.moveTo(1488, 917)
            pydirectinput.click()
        elif state == 'confirm':
            pydirectinput.moveTo(646, 603)
            pydirectinput.click()
        elif state == 'pregame' and (time.time()-stamp) > 180:
            pydirectinput.moveTo(140, 1035)
            pydirectinput.click()
            time.sleep(0.1)
            pydirectinput.moveTo(1430, 417)
            pydirectinput.click()
            time.sleep(0.1)
            pydirectinput.moveTo(707, 600)
            pydirectinput.click()
            time.sleep(10)
            pydirectinput.moveTo(307, 872)
            pydirectinput.click()
        elif state == 'none':
            if state != previous:
                pydirectinput.moveTo(1920,1080)
        previous = state
    else:
        state = ''