import pychrome
import time
import os
print("starting")
#i need to run this at every start  chromium-browser --remote-debugging-port=9222
print("Starting Chrome interaction")
try:
    # Connect to the Chromium browser
    browser = pychrome.Browser(url="http://127.0.0.1:9222")
    tabs = browser.list_tab()

    if not tabs:
        print("No tabs found")
        exit(1)

    tab = tabs[0]
    tab.start()
    # Define the path to the secret file
    secret_file_path = os.path.expanduser("~/.hidden_dir/secret_file.txt")

    # Read the file contents
    with open(secret_file_path, 'r') as file:
        secret_data = file.read()

    # Split the secret data into pos_id and brn
    secret_lines = secret_data.strip().splitlines()
    pos_id = secret_lines[0].split(': ')[1]
    brn = secret_lines[1].split(': ')[1]
    print(brn)
    print(pos_id)

    # JavaScript code to trigger the card check with simulated card data
    js_code = f"""
    window.emvProcessed("{'card_data'}", "{'type'}", "{'pos_id'}", "{'brn'}");
    """
    # Execute the JavaScript code
    result = tab.Runtime.evaluate(expression=js_code)
    print("JavaScript executed:", result)
    
    # Optional: Close the tab connection
    time.sleep(1)
except Exception as e:
    print(f"An error occurred: {e}")