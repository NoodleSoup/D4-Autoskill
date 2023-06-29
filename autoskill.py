import cv2
import numpy as np
import pyautogui
import pyscreenshot as ImageGrab
import json
import time
import ctypes
from colorama import init, Fore
import wmi

init(autoreset=True)  # Initialize colorama
f = wmi.WMI()

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def find_image_on_screen(template, threshold=0.7):
    screenshot = ImageGrab.grab(childprocess=False)
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return max_loc
    return None

def is_target_window_active(target_pid):
    GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow
    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId

    hwnd = GetForegroundWindow()
    pid = ctypes.wintypes.DWORD()
    GetWindowThreadProcessId(hwnd, ctypes.pointer(pid))
    return pid.value == target_pid

def find_process(name = "Diablo IV.exe"):
    process = [proc for proc in f.Win32_Process() if proc.Name == name]
    if (len(process) == 0):
        return
    return process[0].ProcessId

def main():
    config = load_config()
    found_proc = False
    process_id = 0

    while not found_proc:
        process_id = find_process()
        if process_id:
            found_proc = True

    while True:
        if not is_target_window_active(process_id):
            print(Fore.YELLOW + "Target window is not active")
            time.sleep(1)
            continue

        for match in config["matches"]:
            image = cv2.imread(match["image"], cv2.IMREAD_COLOR)
            if find_image_on_screen(image) is not None:
                pyautogui.press(match["key"], 3, 0.0)

        time.sleep(0.1)

if __name__ == "__main__":
    main()
