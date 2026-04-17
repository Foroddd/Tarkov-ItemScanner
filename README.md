# Tarkov Item Lookup

A Python tool that lets you instantly look up any item in Escape from Tarkov by hovering over it and pressing a hotkey. It reads the item tooltip using OCR and opens the tarkov.dev listing for that item in your browser.

## How It Works

1. Hover over an item in Tarkov so the tooltip is visible
2. Press **Shift + F6**
3. Your browser opens the tarkov.dev page for that item

## Requirements

- Python 3
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`

## Installation

1. Clone the repository
```
git clone https://github.com/YOURUSERNAME/tarkov-item-lookup.git
```

2. Install dependencies
```
pip install keyboard pyautogui mss pytesseract Pillow requests
```

3. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) — use the default install path

## Usage

Run the script in a terminal:
```
python main.py
```

Keep the terminal open in the background while playing Tarkov.

## Notes

- If Tesseract is installed to a different path, update this line in `main.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
