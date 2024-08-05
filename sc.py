import subprocess
import time
import pyautogui
from PIL import Image, ImageOps
import pytesseract
import re
# Function to extract PIN and amount from text
def extract_pin_and_amount(text):
    # Define regex patterns for PIN and amount
    pin_pattern = re.compile(r'PIN:\s*(\d{4})')
    amount_pattern = re.compile(r'$\s*([\d,\.]+)')
    
    # Search for PIN and amount in the text
    pin_match = pin_pattern.search(text)
    amount_match = amount_pattern.search(text)
    
    pin = pin_match.group(1) if pin_match else 'PIN not found'
    amount = amount_match.group(1) if amount_match else 'Amount not found'
    
    return pin, amount

# Function to minimize all windows except Chrome
def minimize_except_chrome():
    # Get the list of all window IDs
    windows = subprocess.check_output(['wmctrl', '-l']).decode('utf-8').splitlines()
    chrome_windows = [line for line in windows if 'Google Chrome' in line]
    all_windows = [line.split()[0] for line in windows]

    # Minimize all windows
    for win_id in all_windows:
        subprocess.call(['wmctrl', '-i', '-a', win_id])  # Activate the window
        subprocess.call(['wmctrl', '-i', '-b', 'add,hidden', win_id])  # Minimize the window

    # Restore Chrome windows
    for chrome_win in chrome_windows:
        chrome_win_id = chrome_win.split()[0]
        subprocess.call(['wmctrl', '-i', '-a', chrome_win_id])  # Activate the window
        subprocess.call(['wmctrl', '-i', '-b', 'remove,hidden', chrome_win_id])  # Restore the window

# Minimize all windows except Chrome
minimize_except_chrome()

# Give it a moment to minimize and restore windows
time.sleep(3)

# Take a screenshot of the current screen
screenshot_path = 'screenshot.png'
screenshot = pyautogui.screenshot()
screenshot.save(screenshot_path)
time.sleep(3)
# Open the screenshot image and use pytesseract to extract text
image = Image.open(screenshot_path)
gray_image = ImageOps.grayscale(image)
text = pytesseract.image_to_string(gray_image)
# Extract PIN and amount from the extracted text
pin, amount = extract_pin_and_amount(text)

# Print the results
print(f"Extracted PIN: {pin}")
print(f"Extracted Amount: ${amount}")
# Print the extracted text
#print("Extracted Text:")
#print(text)

# Optional: Save the extracted text to a file
with open('extracted_text.txt', 'w', encoding='utf-8') as file:
    file.write(text)
