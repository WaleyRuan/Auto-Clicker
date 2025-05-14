import threading
import time
import sys
import json
import os
from pynput import mouse, keyboard
import tkinter as tk

# Global state
mouse_controller = mouse.Controller()
clicking = False
click_delay = 0.01
start_key = 's'
stop_key = 'e'
stop_threads = False
SETTINGS_FILE = "clicker_settings.json"

def on_press(key):
    global clicking
    try:
        if hasattr(key, 'char'):
            if key.char == start_key:
                clicking = True
                update_status()
            elif key.char == stop_key:
                clicking = False
                update_status()
    except:
        pass

def auto_clicker():
    while not stop_threads:
        if clicking:
            mouse_controller.click(mouse.Button.left, 1)
            time.sleep(click_delay)
        else:
            time.sleep(0.1)

def listen_keyboard():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def update_settings():
    global start_key, stop_key, click_delay
    start_key = start_key_entry.get()
    stop_key = stop_key_entry.get()
    try:
        click_delay = float(speed_entry.get())
    except ValueError:
        click_delay = 0.01
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, "0.01")
    save_settings()

def toggle_clicking():
    global clicking
    clicking = not clicking
    update_status()

def update_status():
    if clicking:
        status_label.config(text="Status: CLICKING", fg="green")
    else:
        status_label.config(text="Status: IDLE", fg="red")

def exit_program():
    global stop_threads
    stop_threads = True
    root.destroy()
    sys.exit()

def save_settings():
    settings = {
        "start_key": start_key,
        "stop_key": stop_key,
        "click_delay": click_delay
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def load_settings():
    global start_key, stop_key, click_delay
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
                start_key = settings.get("start_key", start_key)
                stop_key = settings.get("stop_key", stop_key)
                click_delay = float(settings.get("click_delay", click_delay))
        except:
            pass

# Load saved settings
load_settings()

# GUI setup
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x280")

tk.Label(root, text="Start Key:").pack()
start_key_entry = tk.Entry(root)
start_key_entry.insert(0, start_key)
start_key_entry.pack()

tk.Label(root, text="Stop Key:").pack()
stop_key_entry = tk.Entry(root)
stop_key_entry.insert(0, stop_key)
stop_key_entry.pack()

tk.Label(root, text="Click Delay (seconds):").pack()
speed_entry = tk.Entry(root)
speed_entry.insert(0, str(click_delay))
speed_entry.pack()

tk.Button(root, text="Apply Settings", command=update_settings).pack(pady=5)
tk.Button(root, text="Toggle Clicking", command=toggle_clicking).pack(pady=5)

status_label = tk.Label(root, text="Status: IDLE", fg="red")
status_label.pack(pady=10)

tk.Button(root, text="Exit", command=exit_program, fg="white", bg="darkred").pack(pady=5)

# Threads
threading.Thread(target=listen_keyboard, daemon=True).start()
threading.Thread(target=auto_clicker, daemon=True).start()

# Start GUI
root.mainloop()
