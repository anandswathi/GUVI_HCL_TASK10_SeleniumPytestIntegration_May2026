"""
TASK 10 - Visit the URL https://www.saucedemo.com/ and login with the following credentials :
	- Username : standard_user
	- Password : secret_sauce

Try to fetch the following using Python Selenium :-
	1.) Title of the webpage
	2.) Current URL of the webpage
	3.) Extract the entire contents of the webpage and save it in a Text file whose name will
	be "Webpage_task_11.txt"

After completing the Selenium automation generate Pytest based test-case reports for both
Positive and Negative test-cases based on the :
	- Title of web application
	- URL of the Homepage
	- URL of the Dashboard after Login with credentials
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Constants
BASE_URL             = "https://www.saucedemo.com/"
TITLE                = "Swag Labs"
USERNAME             = "standard_user"
PASSWORD             = "secret_sauce"

def run_selenium_task_saucedemo():

    # Opening URL - "https://www.saucedemo.com/"
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    driver.maximize_window()

    try:
        # Login to sausedemo.com using given credentials
        driver.get(BASE_URL)
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)

        login_button = driver.find_element(By.ID, "login-button")
        # Checking if the login button is not disabled
        assert not login_button.get_attribute("disabled") == "true"

        login_button.click()
        homepage_header = driver.find_element(By.CSS_SELECTOR, ".title")
        assert homepage_header.text == "Products"
        print("Login to Sauce Demo Successful")

        time.sleep(2)

        # Fetching Title of the webpage
        webpage_title = driver.title
        print("Webpage Title: ",webpage_title)

        # Fetching URL of the current page
        current_page_url = driver.current_url
        print("Current Page URL: ",current_page_url)

        # Fetching the entire contents of the webpage
        webpage_content = driver.page_source

        # Saving webpage contents in a text file Webpage_task_11.txt
        with open("Webpage_task_11.txt", "w", encoding="utf-8") as f:
            f.write(webpage_content)

        print("Page content saved successfully.")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_selenium_task_saucedemo()






