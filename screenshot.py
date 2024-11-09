import os
import keyboard
from PIL import ImageGrab
import datetime

# Define the screenshots directory
screenshot_dir = os.path.join(os.getcwd(), "screenshots")

# Create the directory if it doesn't exist
os.makedirs(screenshot_dir, exist_ok=True)

def take_screenshot():
    # Capture the screen
    screenshot = ImageGrab.grab()
    # Generate a filename with the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
    # Save the screenshot
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")

# Set up the hotkey listener for Ctrl+L
keyboard.add_hotkey('ctrl+l', take_screenshot)

print("Listening for Ctrl+L to take a screenshot... Press any key in this terminal to exit.")

# Wait for any key in the terminal to exit
input()