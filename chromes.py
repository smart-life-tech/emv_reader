import pychrome

# Connect to the Chromium browser
browser = pychrome.Browser(url="http://127.0.0.1:9222")
tab = browser.list_tab()[0]
tab.start()

# Define the JavaScript code to trigger the click
js_code = """
document.getElementById('insert_card').click();
"""

# Execute the JavaScript code
tab.Runtime.evaluate(expression=js_code)

# Close the tab connection
tab.stop()
