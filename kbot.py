import pyautogui
from PIL import ImageGrab
import pygetwindow as gw
import time
import keyboard


def get_window():
    game_window = None
    for window in gw.getAllWindows():
        if "Fish Game" in window.title:
            game_window = window
            return window
    if not game_window:
        return None

def capture_frame():
    screenshot_index = 0
    window = get_window()
    if not window:
        return None
    left, top, right, bottom = window.left, window.top, window.right, window.bottom
    print(left)
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    screenshot.save(f"train//frame_{screenshot_index}.png")
    screenshot_index +=1
    return "Captured!"

def locate(file_name):
    try:
        location = pyautogui.locateOnScreen(file_name, confidence=0.99)
    except pyautogui.ImageNotFoundException:
        return None
    return pyautogui.center(location)

def fishing_bot():
    time_step = 0.1
    while True:
        fish_location = locate('Fish_in_game.png')
        upper_bound_location = locate('Upper_bound.png')
        if fish_location or upper_bound_location:
            try:
                print(f"fish location : {fish_location.y} Upper bound location : {upper_bound_location.y}", end='\n', flush=True)
                distance_to_upper_bound = fish_location.y - upper_bound_location.y
                print(f"Distance to upper bound : {distance_to_upper_bound}")
                if distance_to_upper_bound > 45:
                    keyboard.press_and_release('space')
                    print("Jumping!")

            except AttributeError:
                pass
        time.sleep(time_step)