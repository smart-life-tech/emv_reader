import pychrome
print("starting")
#i need to run this at every start  chromium-browser --remote-debugging-port=9222
try:
    # Connect to the Chromium browser
    browser = pychrome.Browser(url="http://127.0.0.1:9222")
    tabs = browser.list_tab()

    if not tabs:
        print("No tabs found")
        exit(1)

    tab = tabs[0]
    tab.start()

    # Define the JavaScript code to trigger the click
    js_code = """
    document.getElementById('insert_card').click();
    """

    # Execute the JavaScript code
    result = tab.Runtime.evaluate(expression=js_code)
    print(result)

    # Close the tab connection
    #tab.stop()
except Exception as e:
    print(f"An error occurred: {e}")
