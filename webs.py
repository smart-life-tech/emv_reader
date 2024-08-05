from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--remote-debugging-port=9222")

# Set up the WebDriver
service = Service('/usr/bin/chromedriver')  # Update this path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target URL
driver.get('https://chingup.com/rpi_pos/')

try:
    # Wait for the element with the class 'amount-total-bg' to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "centered amount-total amount-total-bg"))
    )

    # Fetch the page source
    page_source = driver.page_source

    print("Page source of the current tab:")
    print(page_source)

    # Now parse the page source to find the amount
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(page_source, 'html.parser')
    amount_element = soup.find('div', class_='centered amount-total amount-total-bg')

    if amount_element:
        amount = amount_element.text.strip()
        print(f"Amount found: {amount}")
    else:
        print("Error getting amount: Element not found.")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
