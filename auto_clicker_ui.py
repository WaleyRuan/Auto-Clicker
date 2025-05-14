import threading
import time
#For closing the program
import sys 
#For mouse and keyboard control
from pynput import mouse, keyboard
#For GUI
import tkinter as tk
#This is a simple auto clicker with a GUI

#Global variables
mouse_controller = mouse.Controller()
clicking = False
click_delay = 0.01
start_key = 's'
stop_key = 'e'


def on_press(key): #keyboard listener
    global clicking, start_key, stop_key
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

def auto_clicker(): #auto clicker function
    while not stop_threads:
        if clicking:
            mouse_controller.click(mouse.Button.left, 1)
            time.sleep(click_delay)
        else:
            time.sleep(0.1)

def listen_keyboard(): # Set up the listener for keyboard events
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def update_settings(): #allow user to change settings, keybinds and speed
    global start_key, stop_key, click_delay
    start_key = start_key_entry.get()
    stop_key = stop_key_entry.get()
    try:
        click_delay = float(speed_entry.get())
    except ValueError:
        click_delay = 0.01
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, "0.01")

def toggle_clicking(): #show/hide clicking
    global clicking
    clicking = not clicking
    update_status()

def update_status(): #update status label with current state (green for clicking, red for idle)
    if clicking:
        status_label.config(text="Status: CLICKING", fg="green")
    else:
        status_label.config(text="Status: IDLE", fg="red")

def exit_program(): #exit program
    global stop_threads
    stop_threads = True
    root.destroy()
    sys.exit()

# UI setup
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x280")

#main window
tk.Label(root, text="Start Key:").pack()
start_key_entry = tk.Entry(root)
start_key_entry.insert(0, "s") #default start key
start_key_entry.pack()

tk.Label(root, text="Stop Key:").pack()
stop_key_entry = tk.Entry(root)
stop_key_entry.insert(0, "e") #default stop key
stop_key_entry.pack()

tk.Label(root, text="Click Delay (seconds):").pack()
speed_entry = tk.Entry(root)
speed_entry.insert(0, "0.01") #default speed
speed_entry.pack()

tk.Button(root, text="Apply Settings", command=update_settings).pack(pady=5)
tk.Button(root, text="Toggle Clicking", command=toggle_clicking).pack(pady=5)

status_label = tk.Label(root, text="Status: IDLE", fg="red")
status_label.pack(pady=10)

tk.Button(root, text="Exit", command=exit_program, fg="white", bg="darkred").pack(pady=5)

# Control flag for threads
stop_threads = False

# Start threads
threading.Thread(target=listen_keyboard, daemon=True).start()
threading.Thread(target=auto_clicker, daemon=True).start()

root.mainloop() # This will keep the program running until the user closes the window
# Note: The program will exit when the window is closed or the exit button is clicked.
