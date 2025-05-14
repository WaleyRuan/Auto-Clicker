import tkinter as tk
import threading
import time
import keyboard
from pynput.mouse import Button, Controller

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
        btn = Button.left if click_type_var.get() == "Left" else Button.right
        limit = int(limit_entry.get()) if click_count_entry.get() else 0
        threading.Thread(target=click_loop, args=(interval, btn, limit), daemon=True).start()
    update_status()
keyboard.add_hotkey('f6', toggle_clicking) #Ctrl+Shift+S to start/stop clicking, Here you can change key bind

#GUI
root = tk.Tk()
root.title("Auto Clicker")
tk.Label(root, text="Click Delay (ms):").pack()
delay_entry = tk.Entry(root)
delay_entry.insert(0, "100") #default delay
delay_entry.pack()

tk.Label(root, text="Click Type:").pack()
click_loop_var = tk.StringVar(value="Left")
tk.OptionMenu(root, click_loop_var, "Left", "Right").pack()

tk.Label(root, text="Click Count (0 for infinite):").pack()
click_count_entry = tk.Entry(root)
click_count_entry.insert(0, "0") #default click count
click_count_entry.pack()

status_label = tk.Label(root, text="Status: IDLE", fg="red")
status_label.pack(pady = 5)

def update_status():
    status_label.config(text="Status: CLICKING" if clicking else "Status: IDLE", fg="green" if clicking else "red")

tk.Button(root, text="Exit", command=lambda: root.quit()).pack(pady=10)
