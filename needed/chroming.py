import time
import pychrome
import os
on=True
off=True
def chrome(card_data, card_type, pos_id, brn):
    time.sleep(3)
    print("Starting Chrome interaction")
    try:
        # Connect to the Chromium browser
        browser = pychrome.Browser(url="http://127.0.0.1:9222")
        tabs = browser.list_tab()

        if not tabs:
            print("No tabs found")
            return
            #exit(1)

        tab = tabs[0]
        tab.start()
    
        # JavaScript code to check if window.cardProcessed exists
        check_js_code = """
        if (typeof window.cardProcessed === 'function') {
            true;
        } else {
            false;
        }
        """
        
        # Execute the JavaScript code to check if the function exists
        result = tab.Runtime.evaluate(expression=check_js_code)
        
        if result['result']['value']:  # If window.cardProcessed exists
            if on :
                print("window.cardProcessed exists, executing the function")
                #os.system('sudo uhubctl -l 1-1 -p 2 -a 1')
                time.sleep(1)
                on=False
                off=True
        else:
            if off:
                print("window.cardProcessed does not exist on this page.")
                #os.system('sudo uhubctl -l 1-1 -p 2 -a 0')
                time.sleep(1)
                off=False
                on = True
        
        # Optional: Close the tab connection
        time.sleep(1)
        #tab.stop()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    while True:
        chrome("card_data", "card_type", "pos_id", "brn")