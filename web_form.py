import requests
import serial
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Configure your serial port and baud rate
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

# Webpage and form details
WEBPAGE_URL = 'https://www.chingup.com/rpi_pos/'
TOTAL_AMOUNT_ID = 'amount'
FORM_ID = 'payment_form'
SERVER_URL = 'https://your-server-endpoint.com/submit'

# Initialize serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Initialize web driver
driver = webdriver.Chrome()
driver.get(WEBPAGE_URL)

def focus_on_amount_field():
    amount_field = driver.find_element(By.ID, TOTAL_AMOUNT_ID)
    amount_field.click()
    amount_field.send_keys(Keys.TAB)

def get_amount_from_form():
    amount_field = driver.find_element(By.ID, TOTAL_AMOUNT_ID)
    return amount_field.get_attribute('value')

def submit_form_to_server(data):
    response = requests.post(SERVER_URL, data=data)
    return response.status_code, response.text

def read_card_data():
    while True:
        if ser.in_waiting > 0:
            data = ser.read(8)  # Adjust size according to your card reader's data length
            if data:
                print("Data received:", data)
                return data

try:
    while True:
        focus_on_amount_field()
        amount = get_amount_from_form()

        print(f"Waiting for card swipe...")

        card_data = read_card_data()
        
        if card_data:
            print("Processing payment...")
            
            # Simulate interaction with Paytrace (Replace with actual Paytrace integration)
            # For example:
            # response = requests.post('https://paytrace.com/api/v1/transaction', data={
            #     'amount': amount,
            #     'card_data': card_data
            # })
            # print("Payment response:", response.status_code, response.text)
            
            print("Submitting form data to server...")
            form_data = {
                'amount': amount,
                'card_data': card_data.hex()
            }
            status_code, response_text = submit_form_to_server(form_data)
            print("Server response:", status_code, response_text)

            # Clear the form for the next transaction
            driver.find_element(By.ID, FORM_ID).reset()

        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping script.")
finally:
    ser.close()
    driver.quit()
