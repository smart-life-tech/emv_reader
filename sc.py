import pyautogui
import pytesseract
from PIL import Image
import time
# Take a screenshot of the current screen
screenshot_path = 'screenshot.png'
print("taking screen shot")
time.sleep(5)
screenshot = pyautogui.screenshot()
screenshot.save(screenshot_path)

# Open the screenshot image and use pytesseract to extract text
image = Image.open(screenshot_path)
text = pytesseract.image_to_string(image)

# Print the extracted text
print("Extracted Text:")
print(text)

# Optional: Save the extracted text to a file
with open('extracted_text.txt', 'w', encoding='utf-8') as file:
    file.write(text)
