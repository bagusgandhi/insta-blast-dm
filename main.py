import time
import pickle
import os
import random
from dotenv import load_dotenv # type: ignore
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from db.queries import insert_profile, mark_as_delivered, has_been_delivered # type: ignore

load_dotenv()

# Configuration
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')
COOKIES_FILE = 'cookies.pkl'
SEARCH_QUERY_LIST = [
  'frozen food jogja', 
  'mixue jogja', 
  'coffee jogja', 
  'penginapan jogja',
  'dapur jogja',
  'hotel jogja'
]

SEARCH_QUERY = random.choice(SEARCH_QUERY_LIST)
MESSAGE_TEXT = """Hendi Teknik - Solusi Elektronik Rusak.
Menerima Servis:
- Kulkas, Freezer, Showcase
- Mesin Ice Cream
- Mesin Cuci
- Kompor Gas
- Pompa Air
- AC
- Setrika
- RiceCooker, oven
- Kipas Angin
- Dispenser
- dll.

Alat Elektronik anda rusak? Hubungi Hendi Teknik
Bisa Servis ditempat dan ada Garansi Servis

WhatsApp: 0889 5742 038
website: henditeknik.id
"""

IMAGE_PATH = os.getenv('IMAGE_PATH')
SELENIUM_HOST = os.getenv('SELENIUM_HOST')
COUNT = os.getenv('MESSAGE_COUNT')


# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

# Initialize WebDriver
driver = webdriver.Remote(
  command_executor=SELENIUM_HOST,
  options=options
)

def handle_notifications_modal():
    try:
        not_now_button = driver.find_element(By.XPATH, '//button[contains(text(), "Not Now")]')
        not_now_button.click()
        time.sleep(2)
    except Exception as e:
        print("No notification modal found or error occurred:", e)

def click_element_by_aria_label(aria_label):
    try:
        element = driver.find_element(By.XPATH, f'//*[@aria-label="{aria_label}"]')
        element.click()
        time.sleep(3)
    except Exception as e:
        print(f"Element with aria-label '{aria_label}' not found or error occurred:", e)

def click_through_profiles():
    try:
        click_element_by_aria_label("Search")
        search_box = driver.find_element(By.XPATH, '//input[@placeholder="Search"]')
        search_box.click()
        search_box.clear()
        search_box.send_keys(SEARCH_QUERY)
        time.sleep(5)
        profile_links = []

        parent_div = driver.find_element(By.XPATH, '//div[contains(@class, "xocp1fn")]')
        child_elements = parent_div.find_elements(By.XPATH, './*')

        for child in child_elements:
          try:
              profile_link = child.find_element(By.TAG_NAME, 'a').get_attribute('href')
              profile_links.append(profile_link)

              # insert data to db
              insert_profile(profile_link)

          except Exception as e:
              print(f"Error occurred while extracting profile link: {e}")

        return profile_links

    except Exception as e:
        print(f"Error occurred during profile navigation: {e}")

def click_send_message_button():
    try:
        # Locate the "Send Message" button and click it
        follow_button = driver.find_element(By.XPATH, '//button[.//div[contains(text(), "Follow")]]')
        follow_button.click()
        time.sleep(2)  # Adjust sleep time as necessary

        send_message_button = driver.find_element(By.XPATH, '//div[contains(text(), "Message") or contains(text(), "Send Message")]')
        send_message_button.click()
        time.sleep(10)  # Adjust sleep time as necessary
    except Exception as e:
        print(f"Error occurred while clicking 'Send Message' button: {e}")

def type_and_send_message():
    try:
        # Locate the contenteditable div and type the message
        message_box = driver.find_element(By.XPATH, '//div[@aria-label="Message" and @contenteditable="true"]')
        message_box.click()
        actions = ActionChains(driver)

        # Type the message, inserting line breaks where appropriate
        for line in MESSAGE_TEXT.split('\n'):
            message_box.send_keys(line)
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
        # actions = ActionChains(driver)
        # message_box.send_keys(MESSAGE_TEXT)
        time.sleep(1)
        
        # Attach image if available
        if os.path.exists(IMAGE_PATH):
            attach_image_button = driver.find_element(By.XPATH, '//input[@type="file"]')
            attach_image_button.send_keys(IMAGE_PATH)
            time.sleep(10)  # Wait for the image to upload

        # Press Enter to send the message
        send_button = driver.find_element(By.XPATH, '//div[contains(text(), "Send") and @role="button"]')
        send_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error occurred while typing/sending the message: {e}")

try:
    # Open Instagram
    driver.get('https://www.instagram.com/')
    time.sleep(2)

    # Load cookies
    cookies = pickle.load(open(COOKIES_FILE, 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Refresh the page to apply cookies
    driver.refresh()
    time.sleep(3)

    handle_notifications_modal()
    time.sleep(2)

    # for testing only
    # driver.get('https://www.instagram.com/nlfkng/')
    # time.sleep(2)
    # click_send_message_button()
    # time.sleep(2)
    # type_and_send_message()

    profile_links = click_through_profiles()
    print(f"Collected {len(profile_links)} profiles.")

    message_count = 0
    for profile_link in profile_links:

        if has_been_delivered(profile_link):
            print(f"Message already delivered to profile: {profile_link}, skipping.")
            continue  # Skip to the next profile

        if message_count >= int(COUNT):
            break

        driver.get(profile_link)
        time.sleep(3)  # Wait for the profile to load

        click_send_message_button()
        time.sleep(3) 
        type_and_send_message()
        time.sleep(3) 
        mark_as_delivered(profile_link)

        message_count += 1
        print(f"Message sent to profile {message_count}: {profile_link}")


finally:
    driver.quit()

print("Completed profile navigation.")

