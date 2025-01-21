import pyautogui
from PIL import ImageGrab
import pygetwindow as gw
import time

actions = ['jump','wait']
directory = r"\train_data"
screenshot_index = 0

def get_window():
    game_window = None
    for window in gw.getAllWindows():
        if "Fish Game" in window.title:
            game_window = window
            return window
    if not game_window:
        return None

def capture_frame():
    global screenshot_index
    window = get_window()
    if not window:
        return None
    left, top, right, bottom = window.left, window.top, window.right, window.bottom
    print(left)
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    screenshot.save(f"train//frame_{screenshot_index}.png")
    screenshot_index +=1
    return "Captured!"


if __name__ == "__main__":
    try:
        while True:
            captured = capture_frame()
            if captured:
                print(captured, end = "\n", flush = True)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass