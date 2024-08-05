from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import usb.core
import usb.util
 
import json

# Configuration details
WEBPAGE_URL = 'https://chingup.com/rpi_pos/'
SERVER_URL = 'http://your-server-endpoint'
CARD_DATA_ID = 'card_data'
AMOUNT_ID = 'amount'
PIN_ID = 'pin'
ZIP_ID = 'zip'
TOTAL_AMOUNT_CLASS = 'amount-total'

# Initialize the web driver with the correct path
chrome_service = ChromeService(executable_path='/usr/bin/chromedriver')
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run headless if no GUI is available
#chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")  # Open port for debugging
# Create a new instance of ChromeDriver
# Set up Chrome options
chrome_options2 = Options()
chrome_options2.add_argument("--remote-debugging-port=9222")  # Open port for debugging

# Path to your ChromeDriver executable
service = ChromeService('/usr/bin/chromedriver')

driver2 = webdriver.Chrome(service=service, options=chrome_options)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.get(WEBPAGE_URL)

def get_amount_from_page():
    print("getting amount from web page rpi")
    try:
        total_amount_element = driver.find_element(By.CLASS_NAME, 'centered amount-total amount-total-bg')
        print("Total amount on the page:", total_amount_element)
        # Extract and print the total amount
        total_amount = total_amount_element.text
        print("Total amount on the page:", total_amount)
        amount_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, TOTAL_AMOUNT_CLASS))
        )
        amount_text = amount_element.text.strip('$').strip()
        return amount_text
    except Exception as e:
        print(f"Error getting amount: {e}")
        return None

def set_card_data_in_form(card_data):
    try:
        data_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, CARD_DATA_ID))
        )
        data_field.send_keys(card_data)
    except Exception as e:
        print(f"Error setting card data: {e}")

def submit_form():
    try:
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form'))
        )
        form.submit()
    except Exception as e:
        print(f"Error submitting form: {e}")

def submit_form_to_server(data):
    try:
        response = requests.post(SERVER_URL, data=data)
        return response.status_code, response.text
    except Exception as e:
        print(f"Error submitting form to server: {e}")
        return None, None

# USB Device details
VENDOR_ID = 0x0acd
PRODUCT_ID = 0x3810

def read_card_data():
    try:
        # Find the USB device with the specified Vendor ID and Product ID
        dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if dev is None:
            raise ValueError('Device not found')

        # Set the active configuration
        dev.set_configuration()

        # Find the IN endpoint (endpoint address should be adjusted based on the device specification)
        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]  # Assuming the interface is at index 0, 0
        ep_in = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )

        if ep_in is None:
            raise ValueError('Endpoint not found')

        # Read data from the IN endpoint
        data = ep_in.read(ep_in.wMaxPacketSize, timeout=5000)
        if data:
            print("Data received:", data)
            return data.hex()  # Return the data as a hexadecimal string

    except usb.core.USBError as e:
        if e.errno == 110:  # Timeout error
            print("Timeout occurred, retrying...")
        else:
            print("USB error:", e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Unexpected error: {e}")

    return "1234567890"

try:
    # Get all open tabs
    windows = driver2.window_handles

    if len(windows) == 0:
        print("No open tabs found.")
    else:
        # Switch to the only open tab
        driver2.switch_to.window(windows[0])

        # Get the page source of the current tab
        page_source = driver2.page_source

        print("Page source of the only open tab:")
        print(page_source)
    # Fetch the list of open tabs
    response = requests.get("http://localhost:9222/json")
    tabs = response.json()

    # Assuming you want the first tab. Modify this if needed to select the right tab.
    tab_id = tabs[0]['id']
    print(tab_id)
   
    # Construct the URL to fetch the page source
    page_source_url = f"http://localhost:9222/devtools/page/{tab_id}"

    # Fetch the page source
    print(page_source_url) 
    time.sleep(1)
    # Execute JavaScript to get the current page source
    page_source = driver.execute_script("return document.documentElement.outerHTML;")

    print("Page source of the current tab opened:")
    print(page_source)
    response = requests.get(page_source_url)
    print(response)
    page_source = response.text

    print("Page source of the current tab:")
    print(page_source)

        
    while True:
        amount = get_amount_from_page()
        if amount:
            print(f"Transaction amount: {amount}")

            print("Waiting for card swipe...")
            card_data = read_card_data()
            
            if card_data:
                set_card_data_in_form(card_data)
                submit_form()

                print("Submitting form data to server...")
                form_data = {
                    'amount': amount,
                    'card_data': card_data
                }
                status_code, response_text = submit_form_to_server(form_data)
                print("Server response:", status_code, response_text)
        else:
            break
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping script.")
finally:
    driver.quit()
