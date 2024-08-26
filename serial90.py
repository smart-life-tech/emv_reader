 
#sudo apt-get install evtest
#sudo evtest
#pip install pynput
from pynput import keyboard

# Initialize a string variable to store the card data
gotten = ''
shift_pressed = False

# Define the callback function for key press events
def on_press(key):
    global gotten, shift_pressed
    try:
        k = key.char  # single-char keys
        if shift_pressed and k.isalpha():  # Handle uppercase letters
            k = k.upper()
    except AttributeError:
        k = key.name  # special keys (like 'shift', 'enter', etc.)
    
    # Check if the Shift key is pressed or released
    if k == 'shift':
        shift_pressed = True
        return
    if k == 'shift_r':
        shift_pressed = True
        return

    # Check if Shift key is released
    if k == 'shift_l' or k == 'shift_r':
        shift_pressed = False
        return

    # Check if the key is a part of the card data
    if k is not None and k not in ['enter','shift', 'shift_l', 'shift_r', 'ctrl', 'alt', 'alt_gr']:
        if k=='space':
            gotten+=" "
        else:
            gotten += k
        #print(f"Key pressed: {k}")
    
    # If 'enter' is pressed, process the data
    if k == 'enter':  # Handle the Enter key (or other termination condition)
        print(f"Card data collected: {gotten}")
        gotten = ''  # Reset the collected data after processing
    
    if k == 'esc':  # Stop the listener on ESC
        return False  # stop listener

# Start the listener
listener = keyboard.Listener(on_press=on_press)
listener.start()  # Start to listen on a separate thread

print("Waiting for card swipe...")

# The main loop can continue to do other work, or just wait for keyboard input
listener.join()  # Keep the program running to listen to the input
