from selenium import webdriver # type: ignore
from dotenv import load_dotenv # type: ignore
import time
import os

load_dotenv()

SELENIUM_HOST = os.getenv('SELENIUM_HOST')

print("Test Execution Started")
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

#maximize the window size
driver.maximize_window()
time.sleep(10)
#navigate to browserstack.com
driver.get("https://www.google.com/")
time.sleep(10)

screenshot_path = "./assets/screenshot.png"
driver.save_screenshot(screenshot_path)

driver.close()
driver.quit()
print("Test Execution Successfully Completed!")