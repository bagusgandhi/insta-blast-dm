import os
from dotenv import load_dotenv # type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
import time
import pickle

load_dotenv()

# Access the variables
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
SELENIUM_HOST = os.getenv('SELENIUM_HOST')

# Configuration
COOKIES_FILE = 'cookies.pkl'

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Remote(
  command_executor=SELENIUM_HOST,
  options=options
)

def handle_notifications_modal():
    try:
        # Wait for the modal to appear and click "Not Now"
        not_now_button = driver.find_element(By.XPATH, '//button[contains(text(), "Not Now")]')
        not_now_button.click()
        time.sleep(2)
    except Exception as e:
        print("No notification modal found or error occurred:", e)



try:
  driver.maximize_window()
  driver.get("https://www.instagram.com/accounts/login/")
  time.sleep(3)

  # Input username and password
  username_input = driver.find_element(By.NAME, 'username')
  password_input = driver.find_element(By.NAME, 'password')
  username_input.send_keys(USERNAME)
  password_input.send_keys(PASSWORD)
  password_input.send_keys(Keys.RETURN)

  time.sleep(10)

  # Navigate to the search page
  driver.get('https://www.instagram.com/')
  time.sleep(3)

  screenshot_path = "./assets/screenshot-login.png"
  driver.save_screenshot(screenshot_path)

  # Handle notifications modal if it appears
  handle_notifications_modal()
  time.sleep(5)
  pickle.dump(driver.get_cookies(), open(COOKIES_FILE, 'wb'))
  
except Exception as e:
  print(e)

finally:
    driver.quit()

print("Completed login.")

