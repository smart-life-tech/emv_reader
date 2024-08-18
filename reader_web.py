import usb.core
import usb.util
import time
import pychrome
import subprocess
# Define the command to start Chromium with the required options
#i need to run this at every start  chromium-browser --remote-debugging-port=9222
chromium_command = [
    "chromium-browser",
    "--remote-debugging-port=9222",
    
    "https://www.chingup.com/rpi_pos/"
]

# Start Chromium using subprocess
try:
    subprocess.Popen(chromium_command)
    print("Chromium browser started successfully.")
except Exception as e:
    print(f"Failed to start Chromium: {e}")

# Define patterns for differentiation might be diffrent for some cards
custom_card_patterns = [
    [2, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0]
]

other_card_patterns = [
    [2, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 8, 0, 9, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 38, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

BUFFER_TIMEOUT = 2  # Timeout in seconds to determine end of data

def is_custom_card(data_chunk):
    return data_chunk in custom_card_patterns

def is_other_card(data_chunk):
    return data_chunk in other_card_patterns

def chrome(card_data):
    print("starting")
    try:
        # Connect to the Chromium browser
        browser = pychrome.Browser(url="http://127.0.0.1:9222")
        tabs = browser.list_tab()

        if not tabs:
            print("No tabs found")
            exit(1)

        tab = tabs[0]
        tab.start()

        # Define the JavaScript code to trigger the click
        js_code = """
        document.getElementById('insert_card').click();
        """
        # Execute the JavaScript code
        result = tab.Runtime.evaluate(expression=js_code)
        print(result)
        
        
        
        # JavaScript code to trigger the card check with simulated card data
        js_code = f"""
        window.chingupCard();
        """
        # Execute the JavaScript code
        result = tab.Runtime.evaluate(expression=js_code)
        print("JavaScript executed:", result)
        
        
        
        # JavaScript code to trigger the card check with simulated card data
        js_code = f"""
        window.emvResponse("{card_data}");
        """
        # Execute the JavaScript code
        result = tab.Runtime.evaluate(expression=js_code)
        print("JavaScript executed:", result)
        
        # Close the tab connection
        #tab.stop()
    except Exception as e:
        print(f"An error occurred: {e}")

# Vendor and Product ID for the AugustaS device
VENDOR_ID = 0x058f
PRODUCT_ID = 0x9540

# Find the USB device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError('Device not found')

# Detach the kernel driver if it's attached
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

# Set the configuration
dev.set_configuration()

# Get the active configuration
cfg = dev.get_active_configuration()

# Access the first interface
intf = cfg.interfaces()[0]

# Find the IN endpoint (interrupt IN endpoint)
ep_in = usb.util.find_descriptor(
    intf,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

if ep_in is None:
    raise ValueError("IN Endpoint not found")

print("Starting data read...")

try:
    chrome('card_data')
    while True:
        try:
            # Read data from the IN endpoint
            data = ep_in.read(ep_in.wMaxPacketSize, timeout=5000)  # Adjust timeout and size if needed
            if data:
                print("Data received:", data)
                # Convert array to list
                data_list = list(data)
                # Save the card data to a .txt file
                with open("card_data.txt", "a") as file:
                    file.write(f"Custom Card Data: {data}\n")
                if len(data)<20:
                    print(f"Data received (Custom Card): {data}")
                    card_data = data  # Replace with actual data if needed
                    chrome(card_data)  # Trigger the Chrome interaction with card data
                
                # Store the data in the buffer
                #data_buffer.extend(data_list)
                
                # Update the last data time
                last_data_time = time.time()
            '''
            else:
                # No data received, check if buffer should be processed
                if time.time() - last_data_time > BUFFER_TIMEOUT:
                    # Process the buffer
                    if len(data_buffer) >= len(custom_card_patterns[0]):
                        # Process each chunk of data
                        while len(data_buffer) >= len(custom_card_patterns[0]):
                            # Extract a chunk of data
                            chunk = data_buffer[:len(custom_card_patterns[0])]
                            data_buffer = data_buffer[len(custom_card_patterns[0]):]
                            
                            if is_custom_card(chunk):
                                print(f"Data received (Custom Card): {chunk}")
                                card_data = "simulated_EMV_data"  # Replace with actual data if needed
                                chrome(card_data)  # Trigger the Chrome interaction with card data
                            elif is_other_card(chunk):
                                print(f"Data received (Other Card): {chunk}")
                            else:
                                print(f"Data received (Unknown Card): {chunk}")
                    '''
                    # Clear the buffer for the next data
                    #data_buffer = []
                    
                    # Update the last data time to avoid continuous processing
                    #last_data_time = time.time()


        except usb.core.USBError as e:
            if e.errno == 110:  # Timeout error
                print("Timeout occurred, retrying...")
            else:
                print("USB error:", e)
        time.sleep(1)  # Delay between reads

finally:
    # Clean up
    usb.util.dispose_resources(dev)
    if dev.is_kernel_driver_active(0):
        dev.attach_kernel_driver(0)
