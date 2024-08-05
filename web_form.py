import usb.core
import usb.util
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# USB Device details
VENDOR_ID = 0x0acd
PRODUCT_ID = 0x3810

# Webpage and form details
WEBPAGE_URL = 'https://www.chingup.com/rpi_pos/'
TOTAL_AMOUNT_CLASS = 'amount-total'
CARD_DATA_ID = 'card_data'
FORM_ID = 'payment_form'
SERVER_URL = 'https://your-server-endpoint.com/submit'

# Initialize the USB device
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

chrome_service = ChromeService(executable_path='/usr/bin/chromedriver')
# Initialize web driver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
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
    try:
        # Read data from the IN endpoint
        data = ep_in.read(ep_in.wMaxPacketSize, timeout=5000)
        if data:
            print("Data received:", data)
            return data
    except usb.core.USBError as e:
        if e.errno == 110:  # Timeout error
            print("Timeout occurred, retrying...")
        else:
            print("USB error:", e)
    return None

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
    usb.util.dispose_resources(dev)
    if dev.is_kernel_driver_active(0):
        dev.attach_kernel_driver(0)
    driver.quit()
