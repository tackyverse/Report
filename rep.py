import os
import subprocess
import json
import time
from pystyle import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Function to load cookies from the JSON file
def load_cookies(driver, cookies_file):
    with open(cookies_file, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            # If the cookie has no domain, set it to the current domain
            if 'domain' not in cookie:
                cookie['domain'] = '.instagram.com'
            driver.add_cookie(cookie)

# Function to report the Instagram profile using cookies
def instagram_reporter_using_cookies(username_report, cookies_file):
    # Set up WebDriver options
    options = Options()
    options.page_load_strategy = 'eager'
    options.headless = False
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--log-level=OFF")

    # Set up the Chrome driver
    driver = uc.Chrome(options=options)
    driver.get(f'https://www.instagram.com/accounts/login/?next=%2F{username_report}%2F&source=desktop_nav')

    # Wait for the page to load
    wait = WebDriverWait(driver, 30)  # Increased wait time

    try:
        # Load cookies if they exist
        print(f"Loading cookies from {cookies_file}")
        load_cookies(driver, cookies_file)

        # Refresh to apply cookies and log in automatically
        driver.refresh()
        time.sleep(5)  # Increased wait time for cookies to apply

        # Wait for profile picture or username to be visible
        profile = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@href,'/accounts/edit/')]")))
        print("Logged in successfully using cookies.")

        # Navigate to the target profile and report
        report_profile(driver, wait)

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()  # Ensure the browser is closed

# Function to report the Instagram profile
def report_profile(driver, wait):
    while True:  # Infinite loop to keep reporting until manually stopped
        try:
            # Locate and click the 3 dots (more options) button
            more_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='More options']")))  # Ensure the correct 'aria-label' or use the right XPath
            more_button.click()

            # Click on the "Report" button
            report_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Report')]")))
            report_button.click()

            # Select "Report Account"
            report_account_option = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), 'Report Account')]")))
            report_account_option.click()

            # Choose the option: "It's posting content that shouldn't be on Instagram"
            posting_content_option = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), 'It\'s posting content that shouldn\'t be on Instagram')]")))
            posting_content_option.click()

            # Choose "It's Spam"
            spam_option = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), 'It’s Spam')]")))
            spam_option.click()

            # Click the "Submit" button
            submit_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Submit')]")))
            submit_button.click()

            # Close the report window after submission
            close_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Close')]")))
            close_button.click()

            print("User has been reported successfully.")

            # Optional: Wait a short time before reporting again (to avoid overloading the system)
            time.sleep(2)  # Adjust the sleep time as needed

        except (TimeoutException, NoSuchElementException) as e:
            # Handle specific exceptions (e.g., element not found or timeout)
            print(f"Error while reporting: {e}")
            driver.save_screenshot('report_error.png')  # Optional: Capture a screenshot on error
            time.sleep(2)  # Wait before retrying after an error (optional)

        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error while reporting: {e}")
            time.sleep(2)  # Wait before retrying after an unexpected error (optional)


# Main execution
if __name__ == "__main__":
    # File that contains the saved cookies (ensure the path is correct)
    cookies_file = 'cookies.json'

    # Ask for the target account username
    username_report = input("Enter the username to report: ")

    # Start the Instagram reporter using cookies
    instagram_reporter_using_cookies(username_report, cookies_file)
