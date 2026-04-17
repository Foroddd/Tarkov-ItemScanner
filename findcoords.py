import pyautogui
import time

# Install pyautogui first: pip install pyautogui
print("Move your mouse to the item name area. Coordinates print every 2 seconds.")
print("Press Ctrl+C to stop.")

while True:
    x, y = pyautogui.position()
    print(f"X: {x}, Y: {y}")
    time.sleep(2)