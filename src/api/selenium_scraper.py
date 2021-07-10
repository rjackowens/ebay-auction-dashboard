import time
from bs4 import BeautifulSoup
from selenium import webdriver
from stop_words import stop_words
from mongo import add_item, delete_collection
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def run_search (search_term: str, min_price: str, max_price: str, stop_words=stop_words.get("general"), headless=False):
    """Run eBay search query with search filters and price constraints."""

    chrome_options = Options()

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(" --disable-web-security")

    # b = webdriver.Chrome(options=chrome_options, executable_path="/Users/jackowens/Documents/status-dashboard/chromedriver")
    b = webdriver.Chrome(options=chrome_options)

    b.get("https://www.ebay.com/sch/ebayadvsearch")
    b.implicitly_wait(2)

    search_query = b.find_element_by_xpath("//*[@id='_nkw']")
    search_query.click()
    search_query.send_keys(search_term + stop_words)

    auction = b.find_element_by_xpath("//*[@id='LH_Auction']")
    auction.click()

    condition_used = b.find_element_by_xpath("//*[@id='LH_ItemConditionUsed']")
    condition_used.click()

    condition_unspecified = b.find_element_by_xpath("//*[@id='LH_ItemConditionNS']")
    condition_unspecified.click()

    number_of_bids_checkbox = b.find_element_by_xpath("//*[@id='LH_NOB']")
    number_of_bids_checkbox.click()
    min_bids = b.find_element_by_xpath("//*[@id='_sabdlo']")
    min_bids.send_keys(Keys.NUMPAD1)
    max_bids = b.find_element_by_xpath("//*[@id='_sabdhi']")
    max_bids.send_keys(Keys.NUMPAD9)
    max_bids.send_keys(Keys.NUMPAD9)


    search_button = b.find_element_by_xpath("//*[@id='searchBtnLowerLnk']")
    search_button.click() # click search button
    # time.sleep(1)

    b.get(b.current_url + f"&_udhi={max_price}&rt=nc&_udlo={min_price}") # set min/max price
    b.get(b.current_url + "&_sop=1") # sort by ending soonest

    # Save Page Source
    page_source_results = b.page_source
    soup = BeautifulSoup(page_source_results, features="lxml")

    # Parse Item Titles
    listings = soup.find_all("li", class_="sresult") # <class 'bs4.element.ResultSet'>

    # Loops through all listings and adds DB properties to lists
    item_titles, item_prices, item_bids, time_remaining, item_urls = [], [], [], [], []
    for listing in listings:
        _item = " " # Removes "New Listing" prefix

        price = listing.find('span', attrs={'class':"bold"}) or None
        if price is not None:
            item_prices.append(price.text)

        title = listing.find('h3', attrs={'class':"lvtitle"}) or None
        if title is not None:
            item_titles.append(title.text)

        bids = listing.find('li', attrs={'class':"lvformat"}) or None
        if bids is not None:
            item_bids.append(bids.text)

        for elem in listing.find_all('span', attrs={'class':"HOURS"}):
            for items in elem:
                try:
                    time_remaining.append(items.partition('\n')[0])
                except TypeError:
                    time_remaining.append("")

        for item in listing.find_all('a', attrs={'class':"vip"}):
            item_urls.append(item["href"])

    # print(item_prices)
    # print(item_titles)
    # print(item_bids)
    # print(time_remaining)
    # print(item_urls)

    delete_collection(search_term)
    for title, price, bids, urls, remaining in zip(item_titles, item_prices, item_bids, item_urls, time_remaining):
        add_item(title, price, bids, urls, remaining, collection_name=search_term)

    b.quit()

# run_search("breguet", "4000", "17650")
