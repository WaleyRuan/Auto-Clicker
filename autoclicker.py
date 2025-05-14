import threading
from pynput import mouse, keyboard
import time

mouse_controller = mouse.Controller()
clicking = False

def on_press(key): #keyboard listener
    global clicking
    try:
        if key.char == 's': #set clicking to True
            clicking = True
        elif key.char == 'e':   
            clicking = False #set clicking to False
    except:
        pass

def auto_clicker(): #auto clicker function
    while True:
        if clicking:
            mouse_controller.click(mouse.Button.left, 1)
            time.sleep(0.00001)  #How fast the clicks are
        else:
            time.sleep(0.1) #idle state

# Set up the listener for keyboard events
def listen_keyboard():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


#Threading
key_listener_thread = threading.Thread(target=listen_keyboard)
key_listener_thread.daemon = True #run in background
key_listener_thread.start()
auto_clicker()
