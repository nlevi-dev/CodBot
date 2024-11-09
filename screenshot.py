import keyboard
from util import take_screenshot

keyboard.add_hotkey('ctrl+l', take_screenshot)
print("Listening for Ctrl+L to take a screenshot... Press any key in this terminal to exit.")
input()