import keyboard
import pyautogui
import mss
from PIL import Image, ImageDraw

# Adjust these until the printed color matches the tooltip border
SAMPLE_OFFSET_X = 13   # pixels left of cursor
SAMPLE_OFFSET_Y = -13   # pixels above cursor

TOLERANCE = 10
SEARCH_W = 300
SEARCH_H = 120

def color_matches(pixel, target, tolerance):
    return all(abs(int(pixel[i]) - int(target[i])) <= tolerance for i in range(3))

def on_hotkey():
    mx, my = pyautogui.position()

    left = mx - SEARCH_W // 2
    top = my - SEARCH_H

    with mss.mss() as sct:
        region = {"left": left, "top": top, "width": SEARCH_W, "height": SEARCH_H}
        screenshot = sct.grab(region)

    img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    draw = ImageDraw.Draw(img)

    # Sample the color at the offset from cursor
    sample_x = (mx + SAMPLE_OFFSET_X) - left
    sample_y = (my + SAMPLE_OFFSET_Y) - top
    sampled_color = img.getpixel((sample_x, sample_y))
    print(f"Sampled color at offset: {sampled_color}")

    # Highlight all pixels matching the sampled color
    match_count = 0
    for y in range(img.height):
        for x in range(img.width):
            if color_matches(img.getpixel((x, y)), sampled_color, TOLERANCE):
                draw.point((x, y), fill=(255, 0, 0))
                match_count += 1

    # Mark the sample point in blue
    draw.ellipse([
        (sample_x - 1, sample_y - 1),
        (sample_x + 1, sample_y + 1)
    ], fill=(0, 0, 255))

    # Mark cursor in green
    cx = mx - left
    cy = my - top
    draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(0, 255, 0), width=2)
    draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(0, 255, 0), width=2)

    img.save("calibration_debug.png")
    print(f"Saved — {match_count} matching pixels found")

keyboard.add_hotkey('shift+f6', on_hotkey)
print("Hover over an item so the tooltip is visible, then press Shift+F6. ESC to quit.")
keyboard.wait('esc')