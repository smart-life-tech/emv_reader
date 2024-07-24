from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (the 'chromedriver' executable should be in your PATH)
driver = webdriver.Chrome()

# Open the webpage
driver.get('https://chingup.com/rpi-pos')

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time as necessary

# Locate the form input field by its name, id, or class (adjust as needed)
input_field = driver.find_element(By.NAME, 'name_of_input_field')  # Change 'name_of_input_field' accordingly

# Submit text to the input field
input_text = 'Your Text Here'
input_field.send_keys(input_text)

# Optionally, submit the form if needed
input_field.send_keys(Keys.RETURN)

# Wait for a while to observe the result (optional)
time.sleep(5)

# Close the browser
driver.quit()
