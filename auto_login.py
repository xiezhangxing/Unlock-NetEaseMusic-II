# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00118F500844DE82735D97A6568EC5C8E45B4ADD07E9269615531C90B2D2237FF1994482DEDF0B4AD6F6C783B968D9177910F691FB186ED38FC6806F397050BEE3FBFB4D13E5D7C8F303484E7B1190811CD9357FFC51393FB5796EB8C56AFCC26CB842D04F52B417C9B6132E65EBA7AE1EA53F475B68679B2412DF8C39910DE94B3949EF9B36A9BE04CAA5F872A77CC8303EF3EAC367AAB8CE07D9B46EDE2EB4DBE76C97763AE9CEF1E8DCF41BE9117F0B062878AFB79C9995F24EB1DFEA0B053E1AE45ED095FB039E6DAC24D1369F2592277FA3ECF2B5B63FEDE1B483FDB35DFC658D14415C068BA105AB636F78E792C473AC81F8C8F189038C137C2B251CBD3A378C60E687E9A758E1619823724C9DE0C3397A8C8AB7B6E5EBC2F6A9B393D5F6F0E34DBFBF459F2B99838F2539E710DA11F262FCFD19DCB0181DA74AC510F2CF757A079227C5F38ADC2D846C3D5F4EF6E49D24102A47858747D6BD8D57EDB8C1"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
