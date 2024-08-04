import requests
import serial
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#from this particular reader, we can only read from it but not write
# Configure your serial port and baud rate
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

# Webpage and form details
WEBPAGE_URL = 'https://www.chingup.com/rpi_pos/'
TOTAL_AMOUNT_CLASS = 'amount-total'
CARD_DATA_ID = 'card_data'
FORM_ID = 'payment_form'
SERVER_URL = 'https://your-server-endpoint.com/submit'

# Initialize serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Initialize web driver
driver = webdriver.Chrome()
driver.get(WEBPAGE_URL)

def get_amount_from_form():
    amount_element = driver.find_element(By.CLASS_NAME, TOTAL_AMOUNT_CLASS)
    amount_text = amount_element.text
    return amount_text.strip('$')

def set_card_data_in_form(card_data):
    card_data_field = driver.find_element(By.ID, CARD_DATA_ID)
    card_data_field.send_keys(card_data)

def submit_form():
    form = driver.find_element(By.TAG_NAME, 'form')
    form.submit()

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
        amount = get_amount_from_form()
        print(f"Transaction amount: {amount}")
        
        print("Waiting for card swipe...")
        card_data = read_card_data()
        
        if card_data:
            card_data_hex = card_data.hex()
            set_card_data_in_form(card_data_hex)
            submit_form()

            print("Submitting form data to server...")
            form_data = {
                'amount': amount,
                'card_data': card_data_hex
            }
            status_code, response_text = submit_form_to_server(form_data)
            print("Server response:", status_code, response_text)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping script.")
finally:
    ser.close()
    driver.quit()
