import os
import sys
import numpy as np
import cv2

# Check if image path is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <path_to_image>")
    sys.exit(1)

# Load the image
image_path = sys.argv[1]
image = cv2.imread(image_path)

# Verify if the image loaded successfully
if image is None:
    print("Error: Could not read the image.")
    sys.exit(1)

# Create a window to display the image
cv2.namedWindow("Image")
cv2.namedWindow("Color", cv2.WINDOW_NORMAL)  # Make the color window resizable
cv2.resizeWindow("Color", 200, 200)  # Set initial size to 200x200
cv2.moveWindow("Color", 50, 50)  # Set initial position to the top left

# Make the color window stay on top
cv2.setWindowProperty("Color", cv2.WND_PROP_TOPMOST, 1)

# Variables to store the cursor position, color, and recorded data
cursor_pos = (0, 0)
cursor_color = (0, 0, 0)
image_with_lines = image.copy()
recorded_data = []  # List to store recorded coordinates, colors, and click type

def on_mouse_move(event, x, y, flags, param):
    global cursor_pos, cursor_color, image_with_lines
    
    # Update cursor position and color
    cursor_pos = (x, y)
    cursor_color = image[y, x] if y < image.shape[0] and x < image.shape[1] else (0, 0, 0)
    
    # Draw crosshair lines in red and update the display image
    image_with_lines = image.copy()
    cv2.line(image_with_lines, (0, y), (image.shape[1], y), (0, 0, 255), 1)  # Horizontal red line
    cv2.line(image_with_lines, (x, 0), (x, image.shape[0]), (0, 0, 255), 1)  # Vertical red line
    
    # Create the color preview with the cursor pixel color
    color_square = np.zeros((200, 200, 3), dtype=np.uint8)
    color_square[:, :] = cursor_color
    cv2.imshow("Color", color_square)

    # Record data on left or right mouse click
    if event == cv2.EVENT_LBUTTONDOWN:
        recorded_data.append((x, y, cursor_color[0], cursor_color[1], cursor_color[2], 0))  # Left click
        print(f"Recorded: Position ({x}, {y}), Color {cursor_color}, Click: Left")
    elif event == cv2.EVENT_RBUTTONDOWN:
        recorded_data.append((x, y, cursor_color[0], cursor_color[1], cursor_color[2], 1))  # Right click
        print(f"Recorded: Position ({x}, {y}), Color {cursor_color}, Click: Right")

# Set the mouse callback to capture cursor movement and clicks
cv2.setMouseCallback("Image", on_mouse_move)

# Keep the windows open until the user presses a key
while True:
    # Display the image with persistent crosshair lines
    cv2.imshow("Image", image_with_lines)
    
    # Break on pressing the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save recorded data to a .npy file
recorded_data = np.array(recorded_data, np.int16)
path = 'profile.npy'
if os.path.isfile(path):
    old = np.load(path)
    recorded_data = np.concatenate([old,recorded_data],0)
np.save(path, recorded_data)

# Cleanup
cv2.destroyAllWindows()
