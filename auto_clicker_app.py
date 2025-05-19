import tkinter as tk
import threading
import time
import keyboard
from pynput.mouse import Button, Controller
#Save Feature
import json
import os

# Main application class
class AutoClickerApp:
    def __init__(self, master):
        self.SETTINGS_FILE = "settings.json" # File to save settings
        self.hotkey = tk.StringVar(value="f6")  #Holds hotkey value
        self.master = master
        self.master.title("Auto Clicker")

        # Internal clicker state
        self.clicking = False               # Tracks whether the auto clicker is active
        self.mouse = Controller()           # Controls the mouse using pynput

        # Tkinter Variables (bind UI to internal state)
        self.delay = tk.StringVar(value="100")          # Click delay in milliseconds
        self.click_type = tk.StringVar(value="Left")    # Left or right click
        self.click_limit = tk.StringVar(value="0")      # Number of clicks (0 = infinite)
        self.status_text = tk.StringVar(value="Status: IDLE")  # Live status display

        self.use_fixed_position = tk.BooleanVar(value=False) # Fixed position toggle
        self.fixed_x = tk.StringVar(value="0") # Fixed X position
        self.fixed_y = tk.StringVar(value="0") # Fixed Y position


        self.load_settings() # Load settings from file if available
        self.bind_hotkey()  # rebind using saved hotkey
        self.setup_ui()     # Build the UI
        self.bind_hotkey()  # Set the global F6 hotkey

    def setup_ui(self):
        # Hotkey input
        tk.Label(self.master, text="Hotkey to Toggle:").pack()
        tk.Entry(self.master, textvariable=self.hotkey).pack()
        tk.Button(self.master, text="Apply Hotkey", command=self.bind_hotkey).pack(pady=4)

        # Delay input
        tk.Label(self.master, text="Click Delay (ms):").pack()
        self.delay_entry = tk.Entry(self.master, textvariable=self.delay)
        self.delay_entry.pack()

        # Click type dropdown (Left/Right)
        tk.Label(self.master, text="Click Type:").pack()
        tk.OptionMenu(self.master, self.click_type, "Left", "Right").pack()

        # Max click count
        tk.Label(self.master, text="Click Count (0 for infinite):").pack()
        self.count_entry = tk.Entry(self.master, textvariable=self.click_limit)
        self.count_entry.pack()
        
        # Fixed position toggle
        tk.Checkbutton(self.master, text="Click at specific position", variable=self.use_fixed_position).pack()

        # Fixed position coordinates
        position_frame = tk.Frame(self.master)
        position_frame.pack(pady=2)

        # X and Y coordinates
        tk.Label(position_frame, text="X:").grid(row=0, column=0)
        tk.Entry(position_frame, textvariable=self.fixed_x, width=6).grid(row=0, column=1)

        tk.Label(position_frame, text="Y:").grid(row=0, column=2)
        tk.Entry(position_frame, textvariable=self.fixed_y, width=6).grid(row=0, column=3)


        # Status label
        self.status_label = tk.Label(self.master, textvariable=self.status_text, fg="red")
        self.status_label.pack(pady=5)

        # Exit button, which also saves settings
        tk.Button(self.master, text="Exit", command=self.exit_app).pack(pady=10)

    def bind_hotkey(self):
        try: # Unbind any existing hotkeys
            keyboard.unhook_all_hotkeys()  
            keyboard.add_hotkey(self.hotkey.get(), self.toggle_clicking) # Bind the new hotkey
        except Exception as e: # Handle any errors
            print("Failed to bind hotkey:", e)

    def toggle_clicking(self):
        # Toggle clicker on or off
        self.clicking = not self.clicking
        if self.clicking:
            # Read delay, click type, and limit from GUI
            delay_sec = float(self.delay.get()) / 1000      # Convert ms to seconds
            max_clicks = int(self.click_limit.get()) if self.click_limit.get().isdigit() else 0
            btn = Button.left if self.click_type.get() == "Left" else Button.right

            # Run clicking logic in a background thread
            thread = threading.Thread(target=self.click_loop, args=(delay_sec, btn, max_clicks), daemon=True)
            thread.start()

        # Update the status label
        self.update_status()

    def click_loop(self, interval, button, limit):
        count = 0 # Initialize click count
        original_pos = self.mouse.position # Store original mouse position

        try: # Get fixed position coordinates
            x = int(self.fixed_x.get()) 
            y = int(self.fixed_y.get())
        except ValueError:
            x, y = 0, 0  # fallback if input is invalid

        while self.clicking: # Loop until clicking is stopped
            # Check if limit is reached
            if limit and count >= limit:
                break
            if self.use_fixed_position.get(): # If fixed position is enabled
                self.mouse.position = (x, y) # Move mouse to fixed position
            self.mouse.click(button) # Perform the click
            count += 1 # Increment click count
            time.sleep(interval) # Wait for the specified interval

        # Optionally restore original mouse position
        if self.use_fixed_position.get():
            self.mouse.position = original_pos
        # Reset clicking state
        self.clicking = False
        self.update_status()


    def update_status(self):
        # Update the status label based on clicker state
        if self.clicking:
            self.status_text.set("Status: CLICKING")
            self.status_label.config(fg="green")
        else:
            self.status_text.set("Status: IDLE")
            self.status_label.config(fg="red")

    def load_settings(self): # Load settings from a JSON file
        if os.path.exists(self.SETTINGS_FILE): # Check if the settings file exists
            try:
                with open(self.SETTINGS_FILE, "r") as f: # Open the file for reading
                    data = json.load(f)
                    self.delay.set(data.get("delay", "100")) # Default delay
                    self.click_type.set(data.get("click_type", "Left")) # Default click type
                    self.click_limit.set(data.get("click_limit", "0")) # Default click limit
                    self.hotkey.set(data.get("hotkey", "f6")) # Default hotkey
                    self.fixed_x.set(data.get("fixed_x", "0")) # Default fixed X position
                    self.fixed_y.set(data.get("fixed_y", "0")) # Default fixed Y position
                    self.use_fixed_position.set(data.get("use_fixed_position", False)) # Default fixed position toggle
            except Exception as e:
                print("Failed to load settings:", e) # Handle any errors

    def save_settings(self): # Save settings to a JSON file
        # Create a dictionary with the current settings
        data = { 
            "delay": self.delay.get(), # Save the delay
            "click_type": self.click_type.get(), # Save the click type
            "click_limit": self.click_limit.get(), # Save the click limit
            "hotkey": self.hotkey.get(), # Save the hotkey
            "fixed_x": self.fixed_x.get(),
            "fixed_y": self.fixed_y.get(),
            "use_fixed_position": self.use_fixed_position.get()
        }
        
        try:
            with open(self.SETTINGS_FILE, "w") as f: # Open the file for writing
                json.dump(data, f) # Save the settings as JSON
        except Exception as e: # Handle any errors
            print("Failed to save settings:", e)

    def exit_app(self): # Exit the application
        self.save_settings() # Save settings before exiting
        self.master.quit() # Close the Tkinter window

# Entry point
def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

# Run app
if __name__ == "__main__":
    main()
