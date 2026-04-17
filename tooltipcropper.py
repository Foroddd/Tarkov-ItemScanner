import keyboard
import pyautogui
import mss
from PIL import Image

SAMPLE_OFFSET_X = 13
SAMPLE_OFFSET_Y = -13
TOLERANCE = 10
SEARCH_W = 500
SEARCH_H = 120

def color_matches(pixel, target, tolerance):
    return all(abs(int(pixel[i]) - int(target[i])) <= tolerance for i in range(3))

def on_hotkey():
    mx, my = pyautogui.position()

    left = mx + SAMPLE_OFFSET_X
    top = my - SEARCH_H

    with mss.mss() as sct:
        region = {"left": left, "top": top, "width": SEARCH_W, "height": SEARCH_H}
        screenshot = sct.grab(region)

    img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

    sample_x = (mx + SAMPLE_OFFSET_X) - left
    sample_y = (my + SAMPLE_OFFSET_Y) - top
    sampled_color = img.getpixel((sample_x, sample_y))
    print(f"Sampled color: {sampled_color}")

    # Scan RIGHT from sample point to find right edge
    right_x = sample_x
    while right_x < img.width and color_matches(img.getpixel((right_x, sample_y)), sampled_color, TOLERANCE):
        right_x += 1

    # Scan UP from sample point to find top edge
    top_y = sample_y
    while top_y > 0 and color_matches(img.getpixel((sample_x, top_y)), sampled_color, TOLERANCE):
        top_y -= 1

    print(f"Crop box: ({sample_x},{top_y}) to ({right_x},{sample_y})")

    cropped = img.crop((sample_x, top_y, right_x, sample_y))
    cropped.save("tooltip_crop.png")
    print("Saved tooltip_crop.png")

keyboard.add_hotkey('shift+f6', on_hotkey)
print("Hover over an item so the tooltip is visible, then press Shift+F6. ESC to quit.")
keyboard.wait('esc')