import cv2
import numpy as np
import keyboard
import win32api
import win32con
import pyautogui
import time

def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.1)

def imagesearch(image, precision=0.8):
    im = pyautogui.screenshot()
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]

    # Calculate the center of the found image
    center_x = max_loc[0] + w // 2
    center_y = max_loc[1] + h // 2
    return [center_x, center_y]

#continuous image searching on screen
def imagesearch_loop(image, timesample, precision=0.8):
    pos = imagesearch(image, precision)
    while pos[0] == -1:
        print(image+" not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
    return pos


try:
    while True:
        pos = imagesearch_loop("lol.png", 0.5)
        if pos[0] != -1:
            print("image found ", "x:", pos[0], "y:", pos[1])
            pyautogui.moveTo(pos[0], pos[1])  # Move to the center of the found image
            click()  # Perform the click action
        else:
            print("Image not found, waiting...")
            time.sleep(0.5)
except KeyboardInterrupt:
    pass