 
#sudo apt-get install evtest
#sudo evtest
#pip install pynput
from pynput import keyboard

# Initialize a string variable to store the card data
gotten = ''

# Define the callback function for key press events
def on_press(key):
    global gotten
    try:
        k = key.char  # single-char keys
    except AttributeError:
        k = key.name  # special keys (like 'esc', 'enter', etc.)

    # Check if the key is a part of the card data
    if k is not None:
        gotten += k
        print(f"Key pressed: {k}")
    
    # If 'enter' or another stop key is pressed, process the data
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
