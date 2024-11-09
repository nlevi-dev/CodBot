import os
import datetime
from PIL import ImageGrab

screenshot_dir = os.path.join(os.getcwd(), "screenshots")
os.makedirs(screenshot_dir, exist_ok=True)

def take_screenshot():
    screenshot = ImageGrab.grab()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")

tolerance = 10

def test_profile(profile, image):
    matched_negative_cnt = 0
    total_negative_cnt = 0
    for point in profile:
        if point[5] == 0 and not (
            image[point[1],point[0],0] >= point[2]-tolerance and image[point[1],point[0],0] <= point[2]+tolerance and 
            image[point[1],point[0],1] >= point[3]-tolerance and image[point[1],point[0],1] <= point[3]+tolerance and 
            image[point[1],point[0],2] >= point[4]-tolerance and image[point[1],point[0],2] <= point[4]+tolerance
        ):
            return False
        if point[5] == 1:
            total_negative_cnt += 1
        if point[5] == 1 and (
            image[point[1],point[0],0] >= point[2]-tolerance and image[point[1],point[0],0] <= point[2]+tolerance and 
            image[point[1],point[0],1] >= point[3]-tolerance and image[point[1],point[0],1] <= point[3]+tolerance and 
            image[point[1],point[0],2] >= point[4]-tolerance and image[point[1],point[0],2] <= point[4]+tolerance
        ):
            matched_negative_cnt += 1
    if matched_negative_cnt == total_negative_cnt and total_negative_cnt > 0:
        return False
    return True

