import sys
import time
import datetime
import pyperclip
from threading import Thread
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options


def get_number():
    """Retuns a random number from webpage"""
    chrome_options = Options()

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(" --disable-web-security")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://numbergenerator.org/")
    time.sleep(1)

    word = driver.find_element_by_xpath("//*[@id='resultVal']")
    print(word.text, file=sys.stderr)


# monday_xpath = "/html/body/div[1]/section/main/div[2]/div/sp-page-row/div/div/span/div/div/div/div/div[2]/div[3]/div/div/div/div[2]/div/div/div/div[2]/div/div[6]"
# source = driver.find_element_by_xpath(monday_xpath).click()

# action = ActionChains(driver)
# action.double_click(source)
# action.double_click(source)

# pyautogui.press('enter')

# pyautogui.press('tab')
# pyautogui.press('tab')
# pyautogui.press('tab')
# pyautogui.press('tab')

# def enter_hours():
#     pyautogui.press('9')
#     pyautogui.press('tab')

# enter_hours()
# enter_hours()
# enter_hours()
# enter_hours()
# enter_hours()

# pyautogui.press('enter')

# time.sleep(8)

# time.sleep(5)

