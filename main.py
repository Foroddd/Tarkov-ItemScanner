import keyboard
import pyautogui
import mss
import pytesseract
import webbrowser
import requests
from PIL import Image
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

SAMPLE_OFFSET_X = 13
SAMPLE_OFFSET_Y = -13
TOLERANCE = 10
SEARCH_W = 500
SEARCH_H = 120

def color_matches(pixel, target, tolerance):
    return all(abs(int(pixel[i]) - int(target[i])) <= tolerance for i in range(3))

def lookup_item(name):
    query = """
    {
        items(name: "%s", limit: 1) {
            name
            link
        }
    }
    """ % name

    try:
        response = requests.post(
            "https://api.tarkov.dev/graphql",
            json={"query": query}
        )
        data = response.json()
        if data is None:
            print("API returned empty response")
            return None
        items = data.get("data", {}).get("items", [])
        if items:
            return items[0]["link"]
        return None
    except Exception as e:
        print(f"API error: {e}")
        return None

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

    right_x = sample_x
    while right_x < img.width and color_matches(img.getpixel((right_x, sample_y)), sampled_color, TOLERANCE):
        right_x += 1

    top_y = sample_y
    while top_y > 0 and color_matches(img.getpixel((sample_x, top_y)), sampled_color, TOLERANCE):
        top_y -= 1

    cropped = img.crop((sample_x, top_y, right_x, sample_y))

    text = pytesseract.image_to_string(cropped, config='--psm 6').strip().replace('\n', ' ').replace('@', '0')
    print(f"Item name: {text}")

    link = lookup_item(text)
    if link:
        print(f"Opening: {link}")
        webbrowser.open(link)
    else:
        print("Item not found on tarkov.dev")

keyboard.add_hotkey('shift+f6', on_hotkey)
print("Hover over an item so the tooltip is visible, then press Shift+F6. ESC to quit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped.")