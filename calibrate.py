import os
import sys
import numpy as np
import cv2

if len(sys.argv) < 2:
    print("Usage: python calibrate.py <path_to_image>")
    sys.exit(1)

image_path = sys.argv[1]
image = cv2.imread(image_path)

cv2.namedWindow("Image")
cv2.namedWindow("Color", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Color", 200, 200)
cv2.moveWindow("Color", 50, 50)
cv2.setWindowProperty("Color", cv2.WND_PROP_TOPMOST, 1)

cursor_pos = (0, 0)
cursor_color = (0, 0, 0)
image_with_lines = image.copy()
recorded_data = []

def on_mouse_move(event, x, y, _, _):
    global cursor_pos, cursor_color, image_with_lines
    cursor_pos = (x, y)
    cursor_color = image[y, x] if y < image.shape[0] and x < image.shape[1] else (0, 0, 0)
    
    image_with_lines = image.copy()
    cv2.line(image_with_lines, (0, y), (image.shape[1], y), (0, 0, 255), 1)
    cv2.line(image_with_lines, (x, 0), (x, image.shape[0]), (0, 0, 255), 1)
    
    color_square = np.zeros((200, 200, 3), dtype=np.uint8)
    color_square[:, :] = cursor_color
    cv2.imshow("Color", color_square)

    if event == cv2.EVENT_LBUTTONDOWN:
        recorded_data.append((x, y, cursor_color[0], cursor_color[1], cursor_color[2], 0))
        print(f"Recorded: Position ({x}, {y}), Color {cursor_color}, Click: Left")
    elif event == cv2.EVENT_RBUTTONDOWN:
        recorded_data.append((x, y, cursor_color[0], cursor_color[1], cursor_color[2], 1))
        print(f"Recorded: Position ({x}, {y}), Color {cursor_color}, Click: Right")

cv2.setMouseCallback("Image", on_mouse_move)

while True:
    cv2.imshow("Image", image_with_lines)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

recorded_data = np.array(recorded_data, np.int16)
path = 'profile.npy'
if os.path.isfile(path):
    old = np.load(path)
    recorded_data = np.concatenate([old,recorded_data],0)
np.save(path, recorded_data)
cv2.destroyAllWindows()