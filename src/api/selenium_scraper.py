import sys
import time
import datetime
from mongo import add_item
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options


def get_number():
    """Retuns a random number from webpage and adds to MongoDB"""
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

    add_item(word.text)
    driver.close()
