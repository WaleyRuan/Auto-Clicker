import tkinter as tk
import threading
import time
import keyboard
from pynput.moouse import Button, Controller

#Global
clicking = False
mouse_controller = Controller()

def click_loop(interval, button, limit):
    global clicking
    count = 0
    while clicking:
        if limit and count >= limit:
            break
        mouse_controller.click(button)
        count += 1
        time.sleep(interval)
    clicking = False
    update_status()

def toggle_clicking():
    global clicking
    clicking = not clicking
    if clicking:
        interval = float(delay_entry.get()) / 1000 #ms to second
        btn Button.left if click_type_var.get() == "Left" else Button.right
        limit = int(limit_entry.get()) if click_count_entry.get() else 0
        threading.Thread(target=click_loop, args=(interval, btn, limit), daemon=True).start()
    update_status()
keyboard.add_hotkey('f6', toggle_clicking) #Ctrl+Shift+S to start/stop clicking, Here you can change key bind

